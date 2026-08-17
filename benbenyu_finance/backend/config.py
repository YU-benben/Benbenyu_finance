"""
笨笨鱼财务系统 - 应用配置模块
从环境变量或 .env 文件读取配置项
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """全局配置类"""

    # 数据库
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "benbenyu_finance"

    # JWT 认证
    secret_key: str = "benbenyu-finance-secret-key-change-in-production"
    access_token_expire_minutes: int = 480

    # 服务
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    @property
    def database_url(self) -> str:
        """构建 SQLAlchemy 数据库连接 URL"""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}?charset=utf8mb4"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局配置单例
settings = Settings()
