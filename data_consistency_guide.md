# SQLAlchemy 2.0 数据一致性指南

## 概述

本指南详细说明了在使用 SQLAlchemy 2.0 进行高考学校数据管理时，如何保证数据插入的一致性和完整性。

## 1. 事务管理

### 1.1 基本事务操作

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import GaokaoDatabase, School, MasterDegree, DoctorDegree, Subject, Specialty

# 创建引擎和会话
engine = create_engine("postgresql://user:password@localhost/gaokao_db")
SessionLocal = sessionmaker(bind=engine)

def insert_school_data_with_transaction(json_data: dict):
    """使用事务插入学校数据"""
    with SessionLocal() as session:
        try:
            # 开始事务
            school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
            
            # 添加主表数据
            session.add(school)
            session.flush()  # 获取主键，但不提交
            
            # 添加关联表数据
            session.add_all(master_degrees)
            session.add_all(doctor_degrees)
            session.add_all(subjects)
            session.add_all(specialties)
            
            # 提交事务
            session.commit()
            print(f"成功插入学校数据: {school.name}")
            
        except Exception as e:
            # 回滚事务
            session.rollback()
            print(f"插入失败，已回滚: {e}")
            raise
```

### 1.2 批量插入事务

```python
def batch_insert_schools(json_files: list):
    """批量插入多个学校数据"""
    with SessionLocal() as session:
        try:
            for json_file in json_files:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
                
                # 检查是否已存在
                existing_school = session.query(School).filter_by(school_id=school.school_id).first()
                if existing_school:
                    print(f"学校 {school.name} 已存在，跳过")
                    continue
                
                session.add(school)
                session.add_all(master_degrees)
                session.add_all(doctor_degrees)
                session.add_all(subjects)
                session.add_all(specialties)
            
            # 批量提交
            session.commit()
            print(f"成功批量插入 {len(json_files)} 个学校数据")
            
        except Exception as e:
            session.rollback()
            print(f"批量插入失败，已回滚: {e}")
            raise
```

## 2. 乐观锁机制

### 2.1 版本控制

```python
def update_school_with_optimistic_lock(school_id: str, updates: dict):
    """使用乐观锁更新学校信息"""
    with SessionLocal() as session:
        try:
            # 查询当前记录
            school = session.query(School).filter_by(school_id=school_id).first()
            if not school:
                raise ValueError(f"学校 {school_id} 不存在")
            
            # 保存当前版本号
            current_version = school.version
            
            # 更新字段
            for key, value in updates.items():
                if hasattr(school, key):
                    setattr(school, key, value)
            
            # 增加版本号
            school.version = current_version + 1
            school.updated_at = datetime.utcnow()
            
            # 提交时检查版本号
            session.commit()
            print(f"成功更新学校 {school.name}，版本: {school.version}")
            
        except Exception as e:
            session.rollback()
            if "version" in str(e).lower():
                print(f"并发更新冲突，请重试: {e}")
            else:
                print(f"更新失败: {e}")
            raise
```

## 3. 数据验证

### 3.1 输入验证

```python
from typing import Optional
import re

class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_school_id(school_id: str) -> bool:
        """验证学校ID格式"""
        if not school_id or len(school_id) > 50:
            return False
        return re.match(r'^[A-Za-z0-9_-]+$', school_id) is not None
    
    @staticmethod
    def validate_email(email: Optional[str]) -> bool:
        """验证邮箱格式"""
        if not email:
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: Optional[str]) -> bool:
        """验证电话格式"""
        if not phone:
            return True
        # 简单的电话号码验证
        pattern = r'^[0-9\-\s\(\)\+]+$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_school_data(school: School) -> list:
        """验证学校数据"""
        errors = []
        
        if not DataValidator.validate_school_id(school.school_id):
            errors.append("学校ID格式无效")
        
        if not school.name or len(school.name) > 200:
            errors.append("学校名称无效")
        
        if not DataValidator.validate_email(school.email):
            errors.append("邮箱格式无效")
        
        if not DataValidator.validate_phone(school.phone):
            errors.append("电话格式无效")
        
        return errors

def insert_school_with_validation(json_data: dict):
    """带验证的学校数据插入"""
    school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
    
    # 验证数据
    errors = DataValidator.validate_school_data(school)
    if errors:
        raise ValueError(f"数据验证失败: {', '.join(errors)}")
    
    with SessionLocal() as session:
        try:
            session.add(school)
            session.add_all(master_degrees)
            session.add_all(doctor_degrees)
            session.add_all(subjects)
            session.add_all(specialties)
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise
```

## 4. 重复数据处理

### 4.1 Upsert 操作

```python
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text

def upsert_school(json_data: dict):
    """插入或更新学校数据"""
    school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
    
    with SessionLocal() as session:
        try:
            # PostgreSQL upsert 示例
            stmt = insert(School).values(
                school_id=school.school_id,
                name=school.name,
                # ... 其他字段
            )
            stmt = stmt.on_conflict_do_update(
                index_elements=['school_id'],
                set_={
                    'name': stmt.excluded.name,
                    'updated_at': datetime.utcnow(),
                    'version': School.version + 1
                }
            )
            session.execute(stmt)
            
            # 处理关联表数据
            # 先删除旧的关联数据
            session.query(MasterDegree).filter_by(school_id=school.school_id).delete()
            session.query(DoctorDegree).filter_by(school_id=school.school_id).delete()
            session.query(Subject).filter_by(school_id=school.school_id).delete()
            session.query(Specialty).filter_by(school_id=school.school_id).delete()
            
            # 插入新的关联数据
            session.add_all(master_degrees)
            session.add_all(doctor_degrees)
            session.add_all(subjects)
            session.add_all(specialties)
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise
```

### 4.2 MySQL Upsert

```python
def upsert_school_mysql(json_data: dict):
    """MySQL 的 upsert 操作"""
    school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
    
    with SessionLocal() as session:
        try:
            # 检查是否存在
            existing_school = session.query(School).filter_by(school_id=school.school_id).first()
            
            if existing_school:
                # 更新现有记录
                for key, value in school.__dict__.items():
                    if not key.startswith('_') and key not in ['id', 'created_at']:
                        setattr(existing_school, key, value)
                existing_school.updated_at = datetime.utcnow()
                existing_school.version += 1
                
                # 删除旧的关联数据
                session.query(MasterDegree).filter_by(school_id=school.school_id).delete()
                session.query(DoctorDegree).filter_by(school_id=school.school_id).delete()
                session.query(Subject).filter_by(school_id=school.school_id).delete()
                session.query(Specialty).filter_by(school_id=school.school_id).delete()
            else:
                # 插入新记录
                session.add(school)
            
            # 插入关联数据
            session.add_all(master_degrees)
            session.add_all(doctor_degrees)
            session.add_all(subjects)
            session.add_all(specialties)
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            raise
```

## 5. 连接池和会话管理

### 5.1 连接池配置

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# 配置连接池
engine = create_engine(
    "postgresql://user:password@localhost/gaokao_db",
    poolclass=QueuePool,
    pool_size=10,          # 连接池大小
    max_overflow=20,       # 最大溢出连接数
    pool_timeout=30,       # 获取连接超时时间
    pool_recycle=3600,     # 连接回收时间
    pool_pre_ping=True,    # 连接前ping检查
    echo=False             # 是否打印SQL
)
```

### 5.2 会话管理最佳实践

```python
from contextlib import contextmanager

@contextmanager
def get_db_session():
    """数据库会话上下文管理器"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# 使用示例
def insert_school_safe(json_data: dict):
    """安全的学校数据插入"""
    with get_db_session() as session:
        school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
        
        session.add(school)
        session.add_all(master_degrees)
        session.add_all(doctor_degrees)
        session.add_all(subjects)
        session.add_all(specialties)
        # 自动提交或回滚
```

## 6. 错误处理和重试机制

### 6.1 重试装饰器

```python
import time
import functools
from sqlalchemy.exc import OperationalError, DisconnectionError

def retry_db_operation(max_retries=3, delay=1):
    """数据库操作重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (OperationalError, DisconnectionError) as e:
                    if attempt == max_retries - 1:
                        raise
                    print(f"数据库操作失败，第 {attempt + 1} 次重试: {e}")
                    time.sleep(delay * (2 ** attempt))  # 指数退避
            return None
        return wrapper
    return decorator

@retry_db_operation(max_retries=3, delay=1)
def insert_school_with_retry(json_data: dict):
    """带重试的学校数据插入"""
    return insert_school_data_with_transaction(json_data)
```

## 7. 数据完整性检查

### 7.1 外键约束检查

```python
def check_data_integrity():
    """检查数据完整性"""
    with SessionLocal() as session:
        # 检查孤立的硕士学位记录
        orphaned_masters = session.query(MasterDegree).filter(
            ~MasterDegree.school_id.in_(
                session.query(School.school_id)
            )
        ).count()
        
        # 检查孤立的博士学位记录
        orphaned_doctors = session.query(DoctorDegree).filter(
            ~DoctorDegree.school_id.in_(
                session.query(School.school_id)
            )
        ).count()
        
        # 检查孤立的学科记录
        orphaned_subjects = session.query(Subject).filter(
            ~Subject.school_id.in_(
                session.query(School.school_id)
            )
        ).count()
        
        # 检查孤立的专业记录
        orphaned_specialties = session.query(Specialty).filter(
            ~Specialty.school_id.in_(
                session.query(School.school_id)
            )
        ).count()
        
        print(f"数据完整性检查结果:")
        print(f"孤立的硕士学位记录: {orphaned_masters}")
        print(f"孤立的博士学位记录: {orphaned_doctors}")
        print(f"孤立的学科记录: {orphaned_subjects}")
        print(f"孤立的专业记录: {orphaned_specialties}")
        
        return {
            'orphaned_masters': orphaned_masters,
            'orphaned_doctors': orphaned_doctors,
            'orphaned_subjects': orphaned_subjects,
            'orphaned_specialties': orphaned_specialties
        }
```

## 8. 性能优化

### 8.1 批量操作

```python
def bulk_insert_schools(json_files: list, batch_size: int = 100):
    """批量插入学校数据"""
    with SessionLocal() as session:
        try:
            schools = []
            all_masters = []
            all_doctors = []
            all_subjects = []
            all_specialties = []
            
            for i, json_file in enumerate(json_files):
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                school, masters, doctors, subjects, specialties = json_to_orm_objects(json_data)
                
                schools.append(school)
                all_masters.extend(masters)
                all_doctors.extend(doctors)
                all_subjects.extend(subjects)
                all_specialties.extend(specialties)
                
                # 批量提交
                if (i + 1) % batch_size == 0:
                    session.bulk_save_objects(schools)
                    session.bulk_save_objects(all_masters)
                    session.bulk_save_objects(all_doctors)
                    session.bulk_save_objects(all_subjects)
                    session.bulk_save_objects(all_specialties)
                    session.commit()
                    
                    # 清空列表
                    schools.clear()
                    all_masters.clear()
                    all_doctors.clear()
                    all_subjects.clear()
                    all_specialties.clear()
            
            # 处理剩余数据
            if schools:
                session.bulk_save_objects(schools)
                session.bulk_save_objects(all_masters)
                session.bulk_save_objects(all_doctors)
                session.bulk_save_objects(all_subjects)
                session.bulk_save_objects(all_specialties)
                session.commit()
            
            print(f"成功批量插入 {len(json_files)} 个学校数据")
            
        except Exception as e:
            session.rollback()
            print(f"批量插入失败: {e}")
            raise
```

## 9. 监控和日志

### 9.1 操作日志

```python
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gaokao_db.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_operation(operation: str, school_id: str = None, success: bool = True, error: str = None):
    """记录数据库操作日志"""
    log_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'operation': operation,
        'school_id': school_id,
        'success': success,
        'error': error
    }
    
    if success:
        logger.info(f"操作成功: {log_data}")
    else:
        logger.error(f"操作失败: {log_data}")

def insert_school_with_logging(json_data: dict):
    """带日志的学校数据插入"""
    school_id = json_data.get('data', {}).get('school_id')
    
    try:
        insert_school_data_with_transaction(json_data)
        log_operation('INSERT_SCHOOL', school_id, True)
    except Exception as e:
        log_operation('INSERT_SCHOOL', school_id, False, str(e))
        raise
```

## 10. 总结

### 数据一致性保证的关键点：

1. **事务管理**: 使用事务确保数据的原子性
2. **乐观锁**: 使用版本号防止并发更新冲突
3. **数据验证**: 在插入前验证数据格式和完整性
4. **重复处理**: 使用 upsert 操作处理重复数据
5. **连接管理**: 正确配置连接池和会话管理
6. **错误处理**: 实现重试机制和完善的错误处理
7. **完整性检查**: 定期检查数据完整性
8. **性能优化**: 使用批量操作提高性能
9. **监控日志**: 记录操作日志便于问题排查

### 最佳实践：

- 始终在事务中进行相关数据的插入
- 使用上下文管理器确保资源正确释放
- 实现适当的重试机制处理临时性错误
- 定期进行数据完整性检查
- 使用批量操作提高大量数据插入的性能
- 记录详细的操作日志便于问题排查