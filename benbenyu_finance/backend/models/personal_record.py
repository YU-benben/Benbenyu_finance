"""
个人用户收支记录 ORM 模型
"""

from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Enum, DateTime, Date, Numeric, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class PersonalRecord(Base):
    __tablename__ = "personal_records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    record_date: Mapped[date] = mapped_column(Date, nullable=False)
    record_type: Mapped[str] = mapped_column(
        Enum("income", "expense", name="personal_record_type"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), default="现金")
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="personal_records")
