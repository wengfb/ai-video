from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # 应用配置
    app_name: str = "AI Video"
    app_version: str = "0.1.0"
    debug: bool = False

    # API 配置
    api_v1_prefix: str = "/api/v1"

    # 数据库配置
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_video"

    # Redis 配置
    redis_url: str = "redis://localhost:6379/0"

    # MinIO 配置
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "ai-video"
    minio_secure: bool = False

    # Celery 配置
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # 端脑云配置
    cephalon_api_url: str = "https://api.cephalon.cloud"
    cephalon_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
