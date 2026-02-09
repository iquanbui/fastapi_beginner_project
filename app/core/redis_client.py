from typing import AsyncGenerator
import redis.asyncio as redis
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.redis_pool = None

    async def connect(self):
        password = settings.REDIS_PASSWORD
        if password == "null" or password == "":
            password = None

        self.redis_pool = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=password,
            encoding="utf-8",
            decode_responses=True,
        )

    async def close(self):
        if self.redis_pool:
            await self.redis_pool.close()

    async def get_client(self) -> redis.Redis:
        if not self.redis_pool:
            await self.connect()
        return self.redis_pool


redis_client = RedisClient()


async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    if not redis_client.redis_pool:
        await redis_client.connect()
    yield redis_client.redis_pool
