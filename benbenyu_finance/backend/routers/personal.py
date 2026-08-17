"""
笨笨鱼财务系统 - 个人用户路由
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from database import get_db
from models import User, UserRole
from schemas import (
    PersonalRecordCreate,
    PersonalRecordUpdate,
    PersonalRecordResponse,
    PersonalStatistics,
)
from dependencies import require_role
from services import personal_service
from utils.excel_export import export_personal_records

router = APIRouter(prefix="/api/personal", tags=["个人用户"])


@router.get("/records", response_model=list[PersonalRecordResponse], summary="查询收支记录")
def get_records(
    start_date: Optional[date] = Query(None, description="开始日期"),
    end_date: Optional[date] = Query(None, description="结束日期"),
    record_type: Optional[str] = Query(None, description="类型: income/expense"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.personal)),
):
    """查询个人收支记录列表"""
    return personal_service.list_records(db, current_user, start_date, end_date, record_type)


@router.post("/records", response_model=PersonalRecordResponse, summary="新增收支记录")
def create_record(
    data: PersonalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.personal)),
):
    """新增一条个人收支记录"""
    return personal_service.create_record(db, current_user, data)


@router.put("/records/{record_id}", response_model=PersonalRecordResponse, summary="更新收支记录")
def update_record(
    record_id: int,
    data: PersonalRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.personal)),
):
    """更新指定个人收支记录"""
    return personal_service.update_record(db, current_user, record_id, data)


@router.delete("/records/{record_id}", summary="删除收支记录")
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.personal)),
):
    """删除指定个人收支记录"""
    personal_service.delete_record(db, current_user, record_id)
    return {"message": "删除成功"}


@router.get("/statistics", response_model=PersonalStatistics, summary="账本统计")
def get_statistics(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.personal)),
):
    """获取个人账本统计数据（总收入、总支出、结余、分类汇总）"""
    return personal_service.get_statistics(db, current_user, start_date, end_date)


@router.get("/export", summary="导出Excel")
def export_excel(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.personal)),
):
    """将个人账本数据导出为 Excel 文件"""
    records = personal_service.list_records(db, current_user, start_date, end_date)
    stats = personal_service.get_statistics(db, current_user, start_date, end_date)

    stats_dict = {
        "total_income": stats.total_income,
        "total_expense": stats.total_expense,
        "balance": stats.balance,
        "record_count": stats.record_count,
        "category_summary": stats.category_summary,
    }

    output = export_personal_records(records, stats_dict)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=personal_ledger.xlsx"},
    )
