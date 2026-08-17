"""
笨笨鱼财务系统 - 演示数据初始化
首次启动时自动创建演示账号与示例记录
"""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from models import User, UserRole, PersonalRecord, OrgRecord, RecordType
from utils.security import hash_password


def seed_demo_data(db: Session):
    """
    初始化演示用户与示例账本数据
    若用户已存在则跳过，避免重复插入
    """
    # ---- 创建演示用户 ----
    demo_users = [
        {
            "username": "personal",
            "password": "123456",
            "role": UserRole.personal,
            "display_name": "张三",
            "org_name": None,
        },
        {
            "username": "org",
            "password": "123456",
            "role": UserRole.organization,
            "display_name": "李四",
            "org_name": "笨笨鱼街道办事处",
        },
    ]

    created_users = {}
    for u in demo_users:
        existing = db.query(User).filter(User.username == u["username"]).first()
        if existing:
            created_users[u["username"]] = existing
            continue

        user = User(
            username=u["username"],
            password_hash=hash_password(u["password"]),
            role=u["role"],
            display_name=u["display_name"],
            org_name=u["org_name"],
        )
        db.add(user)
        db.flush()
        created_users[u["username"]] = user

    db.commit()

    # ---- 个人用户示例记录 ----
    personal_user = created_users.get("personal")
    if personal_user:
        count = db.query(PersonalRecord).filter(
            PersonalRecord.user_id == personal_user.id
        ).count()
        if count == 0:
            samples = [
                PersonalRecord(
                    user_id=personal_user.id,
                    record_date=date(2026, 1, 5),
                    record_type=RecordType.income,
                    category="工资",
                    amount=Decimal("8500.00"),
                    payment_method="银行转账",
                    description="1月工资",
                ),
                PersonalRecord(
                    user_id=personal_user.id,
                    record_date=date(2026, 1, 8),
                    record_type=RecordType.expense,
                    category="餐饮",
                    amount=Decimal("45.50"),
                    payment_method="微信支付",
                    description="午餐",
                ),
                PersonalRecord(
                    user_id=personal_user.id,
                    record_date=date(2026, 1, 10),
                    record_type=RecordType.expense,
                    category="交通",
                    amount=Decimal("120.00"),
                    payment_method="支付宝",
                    description="地铁月卡",
                ),
                PersonalRecord(
                    user_id=personal_user.id,
                    record_date=date(2026, 1, 15),
                    record_type=RecordType.income,
                    category="兼职",
                    amount=Decimal("2000.00"),
                    payment_method="银行转账",
                    description="周末兼职收入",
                ),
            ]
            db.add_all(samples)
            db.commit()

    # ---- 单位用户示例记录 ----
    org_user = created_users.get("org")
    if org_user:
        count = db.query(OrgRecord).filter(OrgRecord.user_id == org_user.id).count()
        if count == 0:
            samples = [
                OrgRecord(
                    user_id=org_user.id,
                    record_date=date(2026, 1, 3),
                    record_type=RecordType.income,
                    voucher_no="PZ20260103001",
                    budget_code="2010101",
                    department="财务科",
                    project_name="基本公共服务",
                    fund_source="一般公共预算",
                    economic_classification="商品和服务支出",
                    functional_classification="一般行政管理事务",
                    amount=Decimal("500000.00"),
                    payee_payer="区财政局",
                    handler="王会计",
                    approver="张主任",
                    description="2026年第一季度预算拨款",
                ),
                OrgRecord(
                    user_id=org_user.id,
                    record_date=date(2026, 1, 12),
                    record_type=RecordType.expense,
                    voucher_no="PZ20260112003",
                    budget_code="30201",
                    department="办公室",
                    project_name="办公设备采购",
                    fund_source="一般公共预算",
                    economic_classification="办公费",
                    functional_classification="一般行政管理事务",
                    amount=Decimal("15800.00"),
                    payee_payer="某某办公用品公司",
                    handler="赵经办",
                    approver="李科长",
                    description="采购打印机及耗材",
                ),
                OrgRecord(
                    user_id=org_user.id,
                    record_date=date(2026, 1, 20),
                    record_type=RecordType.expense,
                    voucher_no="PZ20260120005",
                    budget_code="30211",
                    department="民政科",
                    project_name="社区养老服务",
                    fund_source="专项资金",
                    economic_classification="差旅费",
                    functional_classification="社会保障和就业支出",
                    amount=Decimal("3200.00"),
                    payee_payer="社区服务中心",
                    handler="孙经办",
                    approver="周科长",
                    description="社区养老调研差旅费",
                ),
            ]
            db.add_all(samples)
            db.commit()
