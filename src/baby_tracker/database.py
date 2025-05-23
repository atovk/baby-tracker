"""
数据库配置和连接管理
"""
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import sqlite3
import os

# 数据库URL配置
DATABASE_URL = "sqlite:///data/EasyLog.db"

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,
        "timeout": 20,
    },
    echo=False,  # 设置为True可以看到SQL语句
)

# 启用SQLite外键约束
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA cache_size=1000")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.close()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

def get_db() -> Generator:
    """
    获取数据库会话
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    创建所有表
    """
    # 确保数据目录存在
    os.makedirs("data", exist_ok=True)
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """
    删除所有表（谨慎使用）
    """
    Base.metadata.drop_all(bind=engine)
