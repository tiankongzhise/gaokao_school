# 高考学校数据 SQLAlchemy ORM 模型

本项目提供了用于处理高考学校JSON数据的SQLAlchemy ORM模型，可以方便地将JSON数据转换为数据库对象并进行存储。

## 文件说明

- `models.py` - SQLAlchemy ORM模型定义
- `example_usage.py` - 使用示例脚本
- `README_ORM.md` - 本说明文档

## 数据库表结构

### 主要表

1. **schools** - 学校基本信息表
   - 包含学校的所有基本信息，如名称、类型、地址、联系方式等
   - 包含985/211标识、双一流信息等
   - 包含各种排名信息（软科、QS、校友会等）

2. **master_degrees** - 硕士学位授权点表
   - 存储学校的硕士学位授权点信息
   - 与schools表通过school_id关联

3. **doctor_degrees** - 博士学位授权点表
   - 存储学校的博士学位授权点信息
   - 与schools表通过school_id关联

4. **subjects** - 学科表
   - 存储学校的学科信息
   - 与schools表通过school_id关联

5. **specialties** - 专业表
   - 存储学校的专业详细信息
   - 包含专业排名、特色标识等
   - 与schools表通过school_id关联

## 使用方法

### 1. 安装依赖

```bash
pip install sqlalchemy
# 根据使用的数据库安装对应驱动
# MySQL: pip install pymysql
# PostgreSQL: pip install psycopg2
# SQLite: 内置支持
```

### 2. 基本使用

```python
import json
from models import json_to_orm_objects

# 读取JSON文件
with open('temp_school_info/安徽财经大学.json', 'r', encoding='utf-8') as f:
    json_data = json.load(f)

# 转换为ORM对象
school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)

# 查看学校信息
print(f"学校名称: {school.name}")
print(f"学校类型: {school.type_name}")
print(f"所在地: {school.province_name} {school.city_name}")
```

### 3. 数据库操作

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 创建数据库引擎
engine = create_engine('sqlite:///gaokao_schools.db')

# 创建表结构
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 保存数据
session.add(school)
session.add_all(master_degrees)
session.add_all(doctor_degrees)
session.add_all(subjects)
session.add_all(specialties)

session.commit()
session.close()
```

### 4. 批量处理

```python
import os
import json
from models import json_to_orm_objects

# 批量处理temp_school_info目录下的所有JSON文件
for filename in os.listdir('temp_school_info'):
    if filename.endswith('.json'):
        filepath = os.path.join('temp_school_info', filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        school, master_degrees, doctor_degrees, subjects, specialties = json_to_orm_objects(json_data)
        
        # 处理数据...
        print(f"处理完成: {school.name}")
```

## 数据字段说明

### School表主要字段

- `school_id` - 学校唯一标识
- `name` - 学校名称
- `type_name` - 学校类型（如：财经类、理工类等）
- `school_nature_name` - 学校性质（公办/民办）
- `f985`/`f211` - 985/211标识
- `dual_class` - 双一流信息
- `province_name`/`city_name` - 省份/城市
- `ruanke_rank`/`qs_rank`/`xyh_rank` - 各种排名
- `address` - 详细地址
- `phone`/`email` - 联系方式
- `site`/`school_site` - 官方网站

### Specialty表主要字段

- `special_name` - 专业名称
- `nation_feature` - 是否国家特色专业
- `province_feature` - 是否省级特色专业
- `nation_first_class` - 是否国家一流专业
- `ruanke_rank`/`ruanke_level` - 软科排名和等级
- `limit_year` - 学制年限

## 运行示例

```bash
python example_usage.py
```

这将处理temp_school_info目录下的前3个JSON文件，并显示学校的基本信息。

## 注意事项

1. **数据类型**: 大部分字段使用String类型存储，便于处理各种格式的数据
2. **JSON字段**: 复杂的嵌套数据使用JSON类型存储（如排名信息、链接信息等）
3. **关联关系**: 使用外键建立表之间的关联关系
4. **编码**: 确保JSON文件使用UTF-8编码
5. **错误处理**: 在生产环境中建议添加更完善的错误处理机制

## 扩展建议

1. **数据验证**: 可以添加数据验证逻辑，确保数据的完整性和正确性
2. **索引优化**: 根据查询需求添加适当的数据库索引
3. **数据清洗**: 在转换过程中添加数据清洗和标准化逻辑
4. **批量操作**: 对于大量数据，可以使用批量插入优化性能
5. **缓存机制**: 可以添加缓存机制提高查询性能

## 数据库配置示例

### SQLite（开发环境）
```python
engine = create_engine('sqlite:///gaokao_schools.db')
```

### MySQL
```python
engine = create_engine('mysql+pymysql://username:password@localhost/gaokao_schools?charset=utf8mb4')
```

### PostgreSQL
```python
engine = create_engine('postgresql://username:password@localhost/gaokao_schools')
```

## 许可证

本项目遵循原项目的许可证条款。