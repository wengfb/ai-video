from minio import Minio
from app.core.config import get_settings

settings = get_settings()

minio_client = Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)


def get_minio() -> Minio:
    """获取 MinIO 客户端"""
    return minio_client
