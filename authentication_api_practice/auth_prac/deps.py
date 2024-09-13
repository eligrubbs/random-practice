from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
import redis.asyncio as aioredis


async def get_redis_client() -> Redis:
    REDIS_HOST="localhost"
    REDIS_PORT=6379
    redis = await aioredis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis


RedisDep = Annotated[Redis, Depends(get_redis_client)]
