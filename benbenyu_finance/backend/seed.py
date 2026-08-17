"""
笨笨鱼财务系统 - 初始化脚本
创建演示用户并填充示例数据
"""

from sqlalchemy.orm import Session

from models import User, UserRole, PersonalRecord, OrgRecord, RecordType
from utils.security import hash_password
from decimal import Decimal
from datetime import date


def seed_demo_data(db: Session):
    """
    初始化演示账号与示例数据
    仅在用户不存在时创建，可重复执行
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

    # ---- 填充个人用户示例数据 ----
    personal_user = created_users.get("personal")
    if personal_user and db.query(PersonalRecord).filter(
        PersonalRecord.user_id == personal_user.id
    ).count() == 0:
        sample_personal = [
            PersonalRecord(user_id=personal_user.id, record_date=date(2026, 1, 5), record_type=RecordType.income, category="工资", amount=Decimal("8500.00"), payment_method="银行转账", description="1月工资"),
            PersonalRecord(user_id=personal_user.id, record_date=date(2026, 1, 8), record_type=RecordType.expense, category="餐饮", amount=Decimal("45.50"), payment_method="微信", description="午餐"),
            PersonalRecord(user_id=personal_user.id, record_date=date(2026, 1, 10), record_type=RecordType.expense, category="交通", amount=Decimal("200.00"), payment_method="支付宝", description="地铁月卡"),
            PersonalRecord(user_id=personal_user.id, record_date=date(2026, 1, 15), record_type=RecordType.income, category="兼职", amount=Decimal("1200.00"), payment_method="银行转账", description="周末兼职收入"),
            PersonalRecord(user_id=personal_user.id, record_date=date(2026, 1, 20), record_type=RecordType.expense, category="购物", amount=Decimal("368.00"), payment_method="信用卡", description="日用品采购"),
        ]
        db.add_all(sample_personal)
        db.commit()

    # ---- 填充单位用户示例数据 ----
    org_user = created_users.get("org")
    if org_user and db.query(OrgRecord).filter(
        OrgRecord.user_id == org_user.id
    ).count() == 0:
        sample_org = [
            OrgRecord(user_id=org_user.id, record_date=date(2026, 1, 3), record_type=RecordType.income, voucher_no="PZ20260103001", budget_code="2010101", department="财政所", project_name="基本公共卫生服务", fund_source="一般公共预算", economic_classification="商品和服务支出", functional_classification="医疗卫生", amount=Decimal("500000.00"), payee_payer="区财政局", handler="王五", approver="赵六", description="2026年度基本公卫经费下达"),
            OrgRecord(user_id=org_user.id, record_date=date(2026, 1, 10), record_type=RecordType.expense, voucher_no="PZ20260110001", budget_code="30201", department="党政办", project_name="办公设备采购", fund_source="一般公共预算", economic_classification="办公费", functional_classification="一般行政管理", amount=Decimal("12500.00"), payee_payer="某某办公用品公司", handler="钱七", approver="赵六", description="采购打印机及耗材"),
            OrgRecord(user_id=org_user.id, record_date=date(2026, 1, 15), record_type=RecordType.expense, voucher_no="PZ20260115001", budget_code="30211", department="民政科", project_name="困难群体救助", fund_source="专项资金", economic_classification="对个人和家庭的补助", functional_classification="社会保障", amount=Decimal("80000.00"), payee_payer="辖区困难居民", handler="孙八", approver="赵六", description="春节慰问金发放"),
            OrgRecord(user_id=org_user.id, record_date=date(2026, 1, 20), record_type=RecordType.income, voucher_no="PZ20260120001", budget_code="2120101", department="城建科", project_name="老旧小区改造", fund_source="政府性基金", economic_classification="资本性支出", functional_classification="城乡社区", amount=Decimal("1200000.00"), payee_payer="市住建局", handler="周九", approver="赵六", description="老旧小区改造专项资金"),
        ]
        db.add_all(sample_org)
        db.commit()

    print("[初始化] 演示数据已就绪")
    print("  个人用户: personal / 123456")
    print("  单位用户: org / 123456")
