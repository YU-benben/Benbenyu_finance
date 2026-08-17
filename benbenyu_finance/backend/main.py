"""
笨笨鱼财务系统 - FastAPI 应用入口
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal
from routers import auth, personal, org
from seed import seed_demo_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时建表并初始化演示数据"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="笨笨鱼财务系统 API",
    description="个人与单位财务管理系统后端接口",
    version="1.0.0",
    lifespan=lifespan,
)

# 跨域配置（允许前端独立部署访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(personal.router)
app.include_router(org.router)


@app.get("/", tags=["健康检查"])
def root():
    """API 健康检查"""
    return {"message": "笨笨鱼财务系统 API 运行中", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    from config import settings

    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
