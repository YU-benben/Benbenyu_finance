# 笨笨鱼财务系统

个人与单位（政府）财务管理系统，前后端分离架构。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI + SQLAlchemy + MySQL |
| 前端 | HTML + Vue 3 (CDN) |
| 认证 | JWT + bcrypt |
| 导出 | openpyxl (Excel) |

## 项目目录结构

```
benbenyu-finance/
├── README.md                    # 项目说明文档
├── database/
│   └── init.sql                 # MySQL 建表脚本
├── backend/                     # FastAPI 后端
│   ├── main.py                  # 应用入口
│   ├── config.py                # 配置管理
│   ├── database.py              # 数据库连接
│   ├── dependencies.py          # 认证依赖
│   ├── seed.py                  # 演示数据初始化
│   ├── requirements.txt         # Python 依赖
│   ├── .env.example             # 环境变量示例
│   ├── models/                  # ORM 数据模型
│   │   └── __init__.py
│   ├── schemas/                 # Pydantic 请求/响应模型
│   │   └── __init__.py
│   ├── routers/                 # API 路由
│   │   ├── auth.py              # 登录认证
│   │   ├── personal.py          # 个人用户接口
│   │   └── org.py               # 单位用户接口
│   ├── services/                # 业务逻辑层
│   │   ├── auth_service.py
│   │   ├── personal_service.py
│   │   └── org_service.py
│   └── utils/                   # 工具模块
│       ├── security.py          # 密码/JWT
│       └── excel_export.py      # Excel 导出
└── frontend/                    # Vue3 前端
    ├── index.html               # 登录页
    ├── personal.html            # 个人用户页面
    ├── org.html                 # 单位用户页面
    ├── css/
    │   └── style.css            # 全局样式
    └── js/
        └── api.js               # API 封装
```

## 功能说明

### 1. 登录页面
- 选择身份：**个人用户** / **单位用户**
- 两种角色登录后进入不同页面
- JWT Token 认证，自动跳转

### 2. 个人用户
- 日常收支记账（收入/支出）
- 分类管理（工资、餐饮、交通等）
- 账本统计（总收入、总支出、结余、分类汇总）
- 导出 Excel

### 3. 单位用户
- 政府财政业务管理，字段包括：
  - 凭证号、预算科目编码、部门、项目名称
  - 资金来源、经济分类、功能分类
  - 收款方/付款方、经办人、审批人
- 部门统计、资金来源统计
- 导出 Excel

## 快速启动

### 前置条件

- Python 3.10+
- MySQL 5.7+ / 8.0+
- 现代浏览器（Chrome / Edge / Firefox）

### 第一步：初始化数据库

```bash
# 登录 MySQL 后执行建表脚本
mysql -u root -p < database/init.sql
```

### 第二步：配置后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 复制并编辑环境变量
copy .env.example .env
# 修改 .env 中的 DB_PASSWORD 为你的 MySQL 密码
```

`.env` 示例：

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=benbenyu_finance
```

### 第三步：启动后端

```bash
cd backend
python main.py
```

后端启动后访问：
- API 文档：http://127.0.0.1:8000/docs
- 健康检查：http://127.0.0.1:8000/

> 首次启动会自动创建演示账号和示例数据。

### 第四步：启动前端

前端为纯静态页面，用任意 HTTP 服务器即可：

```bash
cd frontend

# 方式一：Python 内置服务器
python -m http.server 5500

# 方式二：VS Code Live Server 插件
# 右键 index.html -> Open with Live Server
```

浏览器访问：http://127.0.0.1:5500/index.html

## 演示账号

| 身份 | 用户名 | 密码 |
|------|--------|------|
| 个人用户 | personal | 123456 |
| 单位用户 | org | 123456 |

## API 接口概览

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login | 登录 |
| GET | /api/auth/me | 当前用户信息 |
| GET/POST/PUT/DELETE | /api/personal/records | 个人收支 CRUD |
| GET | /api/personal/statistics | 个人统计 |
| GET | /api/personal/export | 个人 Excel 导出 |
| GET/POST/PUT/DELETE | /api/org/records | 单位业务 CRUD |
| GET | /api/org/statistics | 单位统计 |
| GET | /api/org/export | 单位 Excel 导出 |

## 注意事项

1. 前端 `js/api.js` 中 `API_BASE` 默认为 `http://127.0.0.1:8000`，如后端端口不同请修改。
2. 生产环境请更换 `.env` 中的 `SECRET_KEY`。
3. 后端已配置 CORS 允许跨域，前端可独立部署。
