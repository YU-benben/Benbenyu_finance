"""
笨笨鱼财务系统 - 个人用户账本服务
"""

from decimal import Decimal
from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from models import PersonalRecord, RecordType, User
from schemas import (
    PersonalRecordCreate,
    PersonalRecordUpdate,
    PersonalStatistics,
)


def list_records(
    db: Session,
    user: User,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    record_type: Optional[str] = None,
) -> list[PersonalRecord]:
    """查询个人收支记录列表，支持日期和类型筛选"""
    query = db.query(PersonalRecord).filter(PersonalRecord.user_id == user.id)

    if start_date:
        query = query.filter(PersonalRecord.record_date >= start_date)
    if end_date:
        query = query.filter(PersonalRecord.record_date <= end_date)
    if record_type:
        query = query.filter(PersonalRecord.record_type == RecordType(record_type))

    return query.order_by(PersonalRecord.record_date.desc(), PersonalRecord.id.desc()).all()


def create_record(db: Session, user: User, data: PersonalRecordCreate) -> PersonalRecord:
    """创建个人收支记录"""
    record = PersonalRecord(
        user_id=user.id,
        record_date=data.record_date,
        record_type=RecordType(data.record_type),
        category=data.category,
        amount=data.amount,
        payment_method=data.payment_method,
        description=data.description,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_record(
    db: Session, user: User, record_id: int, data: PersonalRecordUpdate
) -> PersonalRecord:
    """更新个人收支记录"""
    record = db.query(PersonalRecord).filter(
        PersonalRecord.id == record_id,
        PersonalRecord.user_id == user.id,
    ).first()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    update_data = data.model_dump(exclude_unset=True)
    if "record_type" in update_data:
        update_data["record_type"] = RecordType(update_data["record_type"])

    for key, value in update_data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_record(db: Session, user: User, record_id: int) -> None:
    """删除个人收支记录"""
    record = db.query(PersonalRecord).filter(
        PersonalRecord.id == record_id,
        PersonalRecord.user_id == user.id,
    ).first()

    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")

    db.delete(record)
    db.commit()


def get_statistics(
    db: Session,
    user: User,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> PersonalStatistics:
    """计算个人账本统计数据"""
    query = db.query(PersonalRecord).filter(PersonalRecord.user_id == user.id)

    if start_date:
        query = query.filter(PersonalRecord.record_date >= start_date)
    if end_date:
        query = query.filter(PersonalRecord.record_date <= end_date)

    records = query.all()

    total_income = sum(
        (r.amount for r in records if r.record_type == RecordType.income),
        Decimal("0"),
    )
    total_expense = sum(
        (r.amount for r in records if r.record_type == RecordType.expense),
        Decimal("0"),
    )

    # 按分类汇总
    category_map: dict[tuple, dict] = {}
    for r in records:
        key = (r.category, r.record_type.value)
        if key not in category_map:
            category_map[key] = {"category": r.category, "record_type": r.record_type.value, "total": Decimal("0"), "count": 0}
        category_map[key]["total"] += r.amount
        category_map[key]["count"] += 1

    category_summary = [
        {**v, "total": v["total"]} for v in category_map.values()
    ]

    return PersonalStatistics(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        record_count=len(records),
        category_summary=category_summary,
    )
