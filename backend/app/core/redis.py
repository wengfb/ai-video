import redis.asyncio as redis
from app.core.config import get_settings

settings = get_settings()

redis_client = redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
)


async def get_redis() -> redis.Redis:
    """获取 Redis 客户端"""
    return redis_client
