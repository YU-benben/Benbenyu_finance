"""
笨笨鱼财务系统 - 单位用户路由
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from schemas import (
    OrgRecordCreate,
    OrgRecordUpdate,
    OrgRecordResponse,
    OrgStatistics,
)
from dependencies import require_role
from services import org_service
from utils.excel_export import export_org_records

router = APIRouter(prefix="/api/org", tags=["单位用户"])


@router.get("/records", response_model=list[OrgRecordResponse], summary="查询财政业务记录")
def get_records(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    record_type: Optional[str] = Query(None, description="类型: income/expense"),
    department: Optional[str] = Query(None, description="部门筛选"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organization)),
):
    """查询单位财政业务记录列表"""
    return org_service.list_records(
        db, current_user, start_date, end_date, record_type, department
    )


@router.post("/records", response_model=OrgRecordResponse, summary="新增财政业务记录")
def create_record(
    data: OrgRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organization)),
):
    """新增一条单位财政业务记录"""
    return org_service.create_record(db, current_user, data)


@router.put("/records/{record_id}", response_model=OrgRecordResponse, summary="更新财政业务记录")
def update_record(
    record_id: int,
    data: OrgRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organization)),
):
    """更新指定单位财政业务记录"""
    return org_service.update_record(db, current_user, record_id, data)


@router.delete("/records/{record_id}", summary="删除财政业务记录")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organization)),
):
    """删除指定单位财政业务记录"""
    org_service.delete_record(db, current_user, record_id)
    return {"message": "删除成功"}


@router.get("/statistics", response_model=OrgStatistics, summary="账本统计")
def get_statistics(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organization)),
):
    """获取单位账本统计数据"""
    return org_service.get_statistics(db, current_user, start_date, end_date)


@router.get("/export", summary="导出Excel")
def export_excel(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organization)),
):
    """将单位财政账本数据导出为 Excel 文件"""
    records = org_service.list_records(db, current_user, start_date, end_date)
    stats = org_service.get_statistics(db, current_user, start_date, end_date)

    stats_dict = {
        "total_income": stats.total_income,
        "total_expense": stats.total_expense,
        "balance": stats.balance,
        "record_count": stats.record_count,
        "department_summary": stats.department_summary,
        "fund_source_summary": stats.fund_source_summary,
    }

    output = export_org_records(records, stats_dict)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=org_ledger.xlsx"},
    )
