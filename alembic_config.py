"""Alembic数据库迁移配置

这个文件展示了如何配置Alembic来管理数据库迁移。
使用Alembic可以帮助你管理数据库schema的版本控制。
"""

from sqlalchemy import create_engine
from alembic import command
from alembic.config import Config
from models import GaokaoDatabase
import os

# 数据库配置
DATABASE_CONFIGS = {
    'sqlite': 'sqlite:///gaokao_schools.db',
    'postgresql': 'postgresql://user:password@localhost/gaokao_db',
    'mysql': 'mysql+pymysql://user:password@localhost/gaokao_db'
}

def init_alembic(database_url: str = None):
    """初始化Alembic配置"""
    if database_url is None:
        database_url = DATABASE_CONFIGS['sqlite']
    
    # 创建alembic.ini配置文件内容
    alembic_ini_content = f"""
# A generic, single database configuration.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration files
# file_template = %%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version number format.  This value may be specified
# as a Python strftime() format string.
# version_num_format = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = {database_url}

[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %%(levelname)-5.5s [%%(name)s] %%(message)s
datefmt = %%H:%%M:%%S
"""
    
    # 写入alembic.ini文件
    with open('alembic.ini', 'w', encoding='utf-8') as f:
        f.write(alembic_ini_content)
    
    print("Alembic配置文件已创建: alembic.ini")

def create_migration_env():
    """创建迁移环境文件"""
    # 创建alembic目录
    os.makedirs('alembic', exist_ok=True)
    
    # 创建env.py文件
    env_py_content = """
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 导入你的模型
from models import GaokaoDatabase

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = GaokaoDatabase.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    \"\"\"Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    \"\"\"
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    \"\"\"Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    \"\"\"
    connectable = engine_from_config(
        config.get_section(config.config_section_name, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""
    
    with open('alembic/env.py', 'w', encoding='utf-8') as f:
        f.write(env_py_content)
    
    # 创建script.py.mako模板
    script_mako_content = """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
"""
    
    with open('alembic/script.py.mako', 'w', encoding='utf-8') as f:
        f.write(script_mako_content)
    
    # 创建versions目录
    os.makedirs('alembic/versions', exist_ok=True)
    
    print("Alembic迁移环境已创建")

def setup_alembic(database_url: str = None):
    """完整设置Alembic"""
    print("正在设置Alembic数据库迁移...")
    
    # 初始化配置
    init_alembic(database_url)
    
    # 创建迁移环境
    create_migration_env()
    
    print("\nAlembic设置完成！")
    print("\n使用方法:")
    print("1. 创建初始迁移: alembic revision --autogenerate -m 'Initial migration'")
    print("2. 应用迁移: alembic upgrade head")
    print("3. 查看迁移历史: alembic history")
    print("4. 回滚迁移: alembic downgrade -1")

if __name__ == "__main__":
    # 设置Alembic
    setup_alembic()