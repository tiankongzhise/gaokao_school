#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：如何使用SQLAlchemy ORM模型处理学校JSON数据

这个脚本演示了如何：
1. 读取JSON文件
2. 转换为ORM对象
3. 创建数据库表结构
4. 将数据保存到数据库（可选）
"""

import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import (
    GaokaoDatabase, School, MasterDegree, DoctorDegree, Subject, Specialty,
    json_to_orm_objects, DataValidator
)
from contextlib import contextmanager
from datetime import datetime
import logging


def load_and_convert_school_data(json_file_path):
    """加载JSON文件并转换为ORM对象"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # 转换为ORM对象
        school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
        
        # 数据验证
        errors = DataValidator.validate_school_data(school)
        if errors:
            logger.warning(f"数据验证警告 {json_file_path}: {', '.join(errors)}")
        
        return school, master_degrees, doctor_degrees, subjects, specialties
        
    except Exception as e:
        logger.error(f"加载文件失败 {json_file_path}: {e}")
        raise

def load_school_json(file_path: str) -> dict:
    """加载学校JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def process_school_data(json_file_path: str):
    """处理单个学校的JSON数据"""
    print(f"正在处理: {json_file_path}")
    
    # 1. 加载JSON数据
    json_data = load_school_json(json_file_path)
    
    # 2. 转换为ORM对象
    school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
    
    # 3. 打印基本信息
    print(f"学校名称: {school.name}")
    print(f"学校ID: {school.school_id}")
    print(f"学校类型: {school.type_name}")
    print(f"学校性质: {school.school_nature_name}")
    print(f"所在地: {school.province_name} {school.city_name}")
    print(f"硕士学位授权点: {len(master_degrees)}个")
    print(f"博士学位授权点: {len(doctor_degrees)}个")
    print(f"专业数量: {len(specialties)}个")
    
    # 4. 打印硕士学位授权点
    if master_degrees:
        print("\n硕士学位授权点:")
        for md in master_degrees:
            print(f"  - {md.name}: {md.num}个")
    
    # 5. 打印博士学位授权点
    if doctor_degrees:
        print("\n博士学位授权点:")
        for dd in doctor_degrees:
            print(f"  - {dd.name}: {dd.num}个")
    
    # 6. 打印部分专业信息
    if specialties:
        print("\n部分专业信息:")
        for i, specialty in enumerate(specialties[:5]):  # 只显示前5个
            print(f"  - {specialty.special_name} ({specialty.level_name})")
            if specialty.nation_feature == '1':
                print(f"    [国家特色专业]")
            if specialty.province_feature == '1':
                print(f"    [省级特色专业]")
        if len(specialties) > 5:
            print(f"  ... 还有 {len(specialties) - 5} 个专业")
    
    print("-" * 50)
    
    return school, master_degrees, doctor_degrees, subjects, specialties


def create_database_tables(engine):
    """创建数据库表结构"""
    print("创建数据库表结构...")
    Base.metadata.create_all(engine)
    print("数据库表结构创建完成")


def save_to_database_with_transaction(school, master_degrees, doctor_degrees, subjects, specialties):
    """使用事务将ORM对象保存到数据库"""
    with get_db_session() as session:
        try:
            # 检查是否已存在
            existing_school = session.query(School).filter_by(school_id=school.school_id).first()
            if existing_school:
                logger.info(f"学校 {school.name} 已存在，跳过插入")
                return existing_school
            
            # 添加学校信息
            session.add(school)
            session.flush()  # 确保获得school的ID
            
            # 添加相关信息
            session.add_all(master_degrees)
            session.add_all(doctor_degrees)
            session.add_all(subjects)
            session.add_all(specialties)
            
            logger.info(f"成功保存学校: {school.name}")
            return school
            
        except Exception as e:
            logger.error(f"保存失败 {school.name}: {e}")
            raise

def upsert_school_data(school, master_degrees, doctor_degrees, subjects, specialties):
    """插入或更新学校数据"""
    with get_db_session() as session:
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
                
                logger.info(f"更新学校: {school.name}")
            else:
                # 插入新记录
                session.add(school)
                logger.info(f"插入新学校: {school.name}")
            
            # 插入关联数据
            session.add_all(master_degrees)
            session.add_all(doctor_degrees)
            session.add_all(subjects)
            session.add_all(specialties)
            
            return existing_school if existing_school else school
            
        except Exception as e:
            logger.error(f"Upsert失败 {school.name}: {e}")
            raise

def save_to_database(engine, school, master_degrees, doctor_degrees, subjects, specialties):
    """将数据保存到数据库（示例）"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 保存学校信息
        session.add(school)
        session.flush()  # 获取school的ID
        
        # 保存相关数据
        session.add_all(master_degrees)
        session.add_all(doctor_degrees)
        session.add_all(subjects)
        session.add_all(specialties)
        
        session.commit()
        print(f"数据已保存到数据库: {school.name}")
        
    except Exception as e:
        session.rollback()
        print(f"保存数据时出错: {e}")
    finally:
        session.close()


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # 创建数据库引擎（支持多种数据库）
    # SQLite 示例
    engine = create_engine('sqlite:///gaokao_schools.db', echo=False)
    
    # PostgreSQL 示例（注释掉）
    # engine = create_engine('postgresql://user:password@localhost/gaokao_db')
    
    # MySQL 示例（注释掉）
    # engine = create_engine('mysql+pymysql://user:password@localhost/gaokao_db')
    
    # 创建数据库表结构
    create_database_tables(engine)
    
    # 创建会话工厂
    global SessionLocal
    SessionLocal = sessionmaker(bind=engine)
    
    # 处理temp_school_info目录下的JSON文件
    temp_school_info_dir = 'temp_school_info'
    
    if not os.path.exists(temp_school_info_dir):
        print(f"目录不存在: {temp_school_info_dir}")
        return
    
    json_files = [f for f in os.listdir(temp_school_info_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"在 {temp_school_info_dir} 目录下没有找到JSON文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件")
    
    # 处理每个JSON文件
    success_count = 0
    error_count = 0
    mode = 'preview'  # 可选: 'preview', 'insert', 'upsert'
    
    for json_file in json_files[:3]:  # 只处理前3个文件作为示例
        json_file_path = os.path.join(temp_school_info_dir, json_file)
        
        try:
            school, master_degrees, doctor_degrees, subjects, specialties = load_and_convert_school_data(json_file_path)
            
            # 根据模式处理数据
            if mode == 'insert':
                save_to_database_with_transaction(school, master_degrees, doctor_degrees, subjects, specialties)
            elif mode == 'upsert':
                upsert_school_data(school, master_degrees, doctor_degrees, subjects, specialties)
            elif mode == 'preview':
                print("预览模式，不保存到数据库")
            
            success_count += 1
            
        except Exception as e:
            print(f"处理文件 {json_file} 时出错: {e}")
            error_count += 1
            continue
    
    print(f"\n处理完成: 成功 {success_count} 个，失败 {error_count} 个")
    
    print("\n处理完成！")
    print("\n使用说明:")
    print("1. 预览模式: 只显示数据，不保存到数据库")
    print("2. 插入模式: 插入新数据，跳过已存在的记录")
    print("3. 更新插入模式: 插入新数据或更新已存在的记录")
    print("\n注意事项:")
    print("1. 这个示例只处理了前3个JSON文件")
    print("2. 修改 mode 变量选择不同的处理模式")
    print("3. 默认使用SQLite数据库，可根据需要修改为其他数据库")
    print("4. 在生产环境中，建议添加更多的错误处理和数据验证")


if __name__ == '__main__':
    main()