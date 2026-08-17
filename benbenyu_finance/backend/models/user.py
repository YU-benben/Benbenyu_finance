"""
用户 ORM 模型
支持 personal（个人用户）和 organization（单位用户）两种角色
"""

from datetime import datetime
from sqlalchemy import String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("personal", "organization", name="user_role"), nullable=False
    )
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    org_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # 关联关系
    personal_records = relationship("PersonalRecord", back_populates="user", cascade="all, delete-orphan")
    org_records = relationship("OrgRecord", back_populates="user", cascade="all, delete-orphan")
