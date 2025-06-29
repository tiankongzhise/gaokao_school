#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据导入脚本
将temp_school_info和temp_zyz_info目录下的JSON数据导入到数据库中
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from zytbxt.db.models import ZyzBase, SchoolInfoTable, ZyzInfoTable
from zytbxt.db.curd import DataImporter


def setup_database(database_url: str = None):
    """
    设置数据库连接
    
    Args:
        database_url: 数据库连接URL，如果为None则使用SQLite
    """
    if database_url is None:
        # 默认使用SQLite数据库
        db_path = current_dir.parent / "gaokao_data.db"
        database_url = f"sqlite:///{db_path}"
    
    print(f"数据库连接: {database_url}")
    
    # 创建数据库引擎
    engine = create_engine(
        database_url,
        echo=False,  # 设置为True可以看到SQL语句
        pool_pre_ping=True
    )
    
    # 创建表结构
    print("创建数据库表结构...")
    ZyzBase.metadata.create_all(engine)
    print("数据库表结构创建完成")
    
    # 创建会话工厂
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal


def import_data_to_database(session_factory, school_info_dir: str, zyz_info_dir: str):
    """
    导入数据到数据库
    
    Args:
        session_factory: 数据库会话工厂
        school_info_dir: 学校信息JSON文件目录
        zyz_info_dir: 专业组信息JSON文件目录
    """
    with session_factory() as session:
        try:
            importer = DataImporter(session)
            
            print("开始导入数据...")
            print(f"学校信息目录: {school_info_dir}")
            print(f"专业组信息目录: {zyz_info_dir}")
            
            # 导入所有数据
            result = importer.import_all_data(school_info_dir, zyz_info_dir)
            
            print("\n=== 导入完成 ===")
            print(f"学校信息记录数: {result['school_count']}")
            print(f"专业组信息记录数: {result['zyz_count']}")
            print(f"总计导入记录数: {result['school_count'] + result['zyz_count']}")
            
            return result
            
        except Exception as e:
            print(f"导入数据时发生错误: {e}")
            session.rollback()
            raise


def main():
    """
    主函数
    """
    print("=== 高考数据导入工具 ===")
    
    # 设置数据目录路径
    school_info_dir = current_dir / "temp_school_info"
    zyz_info_dir = current_dir / "temp_zyz_info"
    
    # 检查目录是否存在
    if not school_info_dir.exists():
        print(f"错误: 学校信息目录不存在: {school_info_dir}")
        return
    
    if not zyz_info_dir.exists():
        print(f"错误: 专业组信息目录不存在: {zyz_info_dir}")
        return
    
    # 统计文件数量
    school_files = list(school_info_dir.glob("*.json"))
    zyz_files = list(zyz_info_dir.glob("*.json"))
    
    print(f"发现学校信息文件: {len(school_files)} 个")
    print(f"发现专业组信息文件: {len(zyz_files)} 个")
    
    if len(school_files) == 0 and len(zyz_files) == 0:
        print("没有找到任何JSON文件，退出")
        return
    
    try:
        # 设置数据库
        # 可以通过环境变量设置数据库URL
        database_url = os.getenv('DATABASE_URL')
        session_factory = setup_database(database_url)
        
        # 导入数据
        result = import_data_to_database(
            session_factory,
            str(school_info_dir),
            str(zyz_info_dir)
        )
        
        print("\n数据导入成功完成！")
        
    except Exception as e:
        print(f"\n导入失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()