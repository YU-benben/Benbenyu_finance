"""
笨笨鱼财务系统 - ORM 数据模型
"""

from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Integer, DateTime, Date, Enum, Numeric, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from database import Base


class UserRole(str, enum.Enum):
    """用户角色枚举"""
    personal = "personal"
    organization = "organization"


class RecordType(str, enum.Enum):
    """收支类型枚举"""
    income = "income"
    expense = "expense"


class User(Base):
    """用户表 ORM 模型"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    org_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 关联关系
    personal_records: Mapped[list["PersonalRecord"]] = relationship(
        "PersonalRecord", back_populates="user", cascade="all, delete-orphan"
    )
    org_records: Mapped[list["OrgRecord"]] = relationship(
        "OrgRecord", back_populates="user", cascade="all, delete-orphan"
    )


class PersonalRecord(Base):
    """个人用户收支记录 ORM 模型"""

    __tablename__ = "personal_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    record_type: Mapped[RecordType] = mapped_column(Enum(RecordType), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), default="现金")
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="personal_records")


class OrgRecord(Base):
    """单位用户财政业务记录 ORM 模型"""

    __tablename__ = "org_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    record_type: Mapped[RecordType] = mapped_column(Enum(RecordType), nullable=False)
    voucher_no: Mapped[str | None] = mapped_column(String(50), nullable=True)
    budget_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    project_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    fund_source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    economic_classification: Mapped[str | None] = mapped_column(String(100), nullable=True)
    functional_classification: Mapped[str | None] = mapped_column(String(100), nullable=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    payee_payer: Mapped[str | None] = mapped_column(String(200), nullable=True)
    handler: Mapped[str | None] = mapped_column(String(50), nullable=True)
    approver: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship("User", back_populates="org_records")
