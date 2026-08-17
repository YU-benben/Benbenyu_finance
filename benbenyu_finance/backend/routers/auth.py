"""
笨笨鱼财务系统 - 认证路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import LoginRequest, TokenResponse, UserInfo
from services.auth_service import authenticate_user
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=TokenResponse, summary="用户登录")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录接口
    - 需选择身份：personal（个人用户）或 organization（单位用户）
    - 返回 JWT 访问令牌
    """
    return authenticate_user(db, login_data)


@router.get("/me", response_model=UserInfo, summary="获取当前用户信息")
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户的基本信息"""
    return current_user
