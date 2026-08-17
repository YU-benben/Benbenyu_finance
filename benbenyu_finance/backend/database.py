"""
笨笨鱼财务系统 - 数据库连接与会话管理
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings

# 创建数据库引擎
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,       # 连接池自动检测断线重连
    pool_recycle=3600,        # 每小时回收连接
    echo=False,
)

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """ORM 基类"""
    pass


def get_db():
    """
    FastAPI 依赖注入：获取数据库会话
    请求结束后自动关闭连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
