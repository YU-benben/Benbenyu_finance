"""
笨笨鱼财务系统 - Pydantic 请求/响应模型
"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field


# ===================== 认证相关 =====================

class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    password: str = Field(..., min_length=1, description="密码")
    role: Literal["personal", "organization"] = Field(..., description="登录身份")


class TokenResponse(BaseModel):
    """登录成功返回 Token"""
    access_token: str
    token_type: str = "bearer"
    role: str
    display_name: str
    org_name: Optional[str] = None


class UserInfo(BaseModel):
    """当前用户信息"""
    id: int
    username: str
    role: str
    display_name: str
    org_name: Optional[str] = None

    class Config:
        from_attributes = True


# ===================== 个人用户记录 =====================

class PersonalRecordCreate(BaseModel):
    """创建个人收支记录"""
    record_date: date
    record_type: Literal["income", "expense"]
    category: str = Field(..., max_length=50)
    amount: Decimal = Field(..., gt=0)
    payment_method: str = Field(default="现金", max_length=30)
    description: Optional[str] = Field(default=None, max_length=500)


class PersonalRecordUpdate(BaseModel):
    """更新个人收支记录"""
    record_date: Optional[date] = None
    record_type: Optional[Literal["income", "expense"]] = None
    category: Optional[str] = Field(default=None, max_length=50)
    amount: Optional[Decimal] = Field(default=None, gt=0)
    payment_method: Optional[str] = Field(default=None, max_length=30)
    description: Optional[str] = Field(default=None, max_length=500)


class PersonalRecordResponse(BaseModel):
    """个人收支记录响应"""
    id: int
    user_id: int
    record_date: date
    record_type: str
    category: str
    amount: Decimal
    payment_method: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class PersonalStatistics(BaseModel):
    """个人账本统计"""
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    record_count: int
    category_summary: list[dict]


# ===================== 单位用户记录 =====================

class OrgRecordCreate(BaseModel):
    """创建单位财政业务记录"""
    record_date: date
    record_type: Literal["income", "expense"]
    voucher_no: Optional[str] = Field(default=None, max_length=50)
    budget_code: Optional[str] = Field(default=None, max_length=50)
    department: Optional[str] = Field(default=None, max_length=100)
    project_name: Optional[str] = Field(default=None, max_length=200)
    fund_source: Optional[str] = Field(default=None, max_length=100)
    economic_classification: Optional[str] = Field(default=None, max_length=100)
    functional_classification: Optional[str] = Field(default=None, max_length=100)
    amount: Decimal = Field(..., gt=0)
    payee_payer: Optional[str] = Field(default=None, max_length=200)
    handler: Optional[str] = Field(default=None, max_length=50)
    approver: Optional[str] = Field(default=None, max_length=50)
    description: Optional[str] = Field(default=None, max_length=500)


class OrgRecordUpdate(BaseModel):
    """更新单位财政业务记录"""
    record_date: Optional[date] = None
    record_type: Optional[Literal["income", "expense"]] = None
    voucher_no: Optional[str] = None
    budget_code: Optional[str] = None
    department: Optional[str] = None
    project_name: Optional[str] = None
    fund_source: Optional[str] = None
    economic_classification: Optional[str] = None
    functional_classification: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    payee_payer: Optional[str] = None
    handler: Optional[str] = None
    approver: Optional[str] = None
    description: Optional[str] = None


class OrgRecordResponse(BaseModel):
    """单位财政业务记录响应"""
    id: int
    user_id: int
    record_date: date
    record_type: str
    voucher_no: Optional[str]
    budget_code: Optional[str]
    department: Optional[str]
    project_name: Optional[str]
    fund_source: Optional[str]
    economic_classification: Optional[str]
    functional_classification: Optional[str]
    amount: Decimal
    payee_payer: Optional[str]
    handler: Optional[str]
    approver: Optional[str]
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class OrgStatistics(BaseModel):
    """单位账本统计"""
    total_income: Decimal
    total_expense: Decimal
    balance: Decimal
    record_count: int
    department_summary: list[dict]
    fund_source_summary: list[dict]
