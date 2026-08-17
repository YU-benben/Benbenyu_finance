"""
笨笨鱼财务系统 - 认证服务
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import User, UserRole
from schemas import LoginRequest, TokenResponse
from utils.security import verify_password, create_access_token


def authenticate_user(db: Session, login_data: LoginRequest) -> TokenResponse:
    """
    用户登录认证
    1. 查找用户
    2. 验证密码
    3. 验证角色与所选身份一致
    4. 签发 JWT
    """
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    # 验证所选身份与账号角色一致
    expected_role = UserRole(login_data.role)
    if user.role != expected_role:
        role_names = {"personal": "个人用户", "organization": "单位用户"}
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"该账号不是{role_names.get(login_data.role, login_data.role)}，请选择正确身份",
        )

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})

    return TokenResponse(
        access_token=token,
        role=user.role.value,
        display_name=user.display_name,
        org_name=user.org_name,
    )
