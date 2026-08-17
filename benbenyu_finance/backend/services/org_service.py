"""
笨笨鱼财务系统 - 单位用户财政业务服务
"""

from decimal import Decimal
from datetime import date
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import OrgRecord, RecordType, User
from schemas import OrgRecordCreate, OrgRecordUpdate, OrgStatistics


def list_records(
    db: Session,
    user: User,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    record_type: Optional[str] = None,
    department: Optional[str] = None,
) -> list[OrgRecord]:
    """查询单位财政业务记录列表"""
    query = db.query(OrgRecord).filter(OrgRecord.user_id == user.id)

    if start_date:
        query = query.filter(OrgRecord.record_date >= start_date)
    if end_date:
        query = query.filter(OrgRecord.record_date <= end_date)
    if record_type:
        query = query.filter(OrgRecord.record_type == RecordType(record_type))
    if department:
        query = query.filter(OrgRecord.department.like(f"%{department}%"))

    return query.order_by(OrgRecord.record_date.desc(), OrgRecord.id.desc()).all()


def create_record(db: Session, user: User, data: OrgRecordCreate) -> OrgRecord:
    """创建单位财政业务记录"""
    record = OrgRecord(
        user_id=user.id,
        record_date=data.record_date,
        record_type=RecordType(data.record_type),
        voucher_no=data.voucher_no,
        budget_code=data.budget_code,
        department=data.department,
        project_name=data.project_name,
        fund_source=data.fund_source,
        economic_classification=data.economic_classification,
        functional_classification=data.functional_classification,
        amount=data.amount,
        payee_payer=data.payee_payer,
        handler=data.handler,
        approver=data.approver,
        description=data.description,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def update_record(
    db: Session, user: User, record_id: int, data: OrgRecordUpdate
) -> OrgRecord:
    """更新单位财政业务记录"""
    record = db.query(OrgRecord).filter(
        OrgRecord.id == record_id,
        OrgRecord.user_id == user.id,
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
    """删除单位财政业务记录"""
    record = db.query(OrgRecord).filter(
        OrgRecord.id == record_id,
        OrgRecord.user_id == user.id,
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
) -> OrgStatistics:
    """计算单位账本统计数据"""
    query = db.query(OrgRecord).filter(OrgRecord.user_id == user.id)

    if start_date:
        query = query.filter(OrgRecord.record_date >= start_date)
    if end_date:
        query = query.filter(OrgRecord.record_date <= end_date)

    records = query.all()

    total_income = sum(
        (r.amount for r in records if r.record_type == RecordType.income),
        Decimal("0"),
    )
    total_expense = sum(
        (r.amount for r in records if r.record_type == RecordType.expense),
        Decimal("0"),
    )

    # 按部门汇总
    dept_map: dict[str, dict] = {}
    for r in records:
        dept = r.department or "未分类"
        if dept not in dept_map:
            dept_map[dept] = {"department": dept, "income": Decimal("0"), "expense": Decimal("0"), "count": 0}
        if r.record_type == RecordType.income:
            dept_map[dept]["income"] += r.amount
        else:
            dept_map[dept]["expense"] += r.amount
        dept_map[dept]["count"] += 1

    # 按资金来源汇总
    fund_map: dict[str, dict] = {}
    for r in records:
        fund = r.fund_source or "未分类"
        if fund not in fund_map:
            fund_map[fund] = {"fund_source": fund, "total": Decimal("0"), "count": 0}
        fund_map[fund]["total"] += r.amount
        fund_map[fund]["count"] += 1

    return OrgStatistics(
        total_income=total_income,
        total_expense=total_expense,
        balance=total_income - total_expense,
        record_count=len(records),
        department_summary=list(dept_map.values()),
        fund_source_summary=list(fund_map.values()),
    )
