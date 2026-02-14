import redis.asyncio as redis
import fakeredis.aioredis
from app.config import settings


class RedisClient:
    def __init__(self):
        if settings.environment == "Development":
            self.client = fakeredis.aioredis.FakeRedis(decode_responses=True)

        if settings.environment == "Production":
            self.client = redis.Redis(host=settings.redis_url,
                                      port=settings.redis_port,
                                      db=settings.redis_db,
                                      decode_responses=True)

    async def get(self, key: str):
        return await self.client.get(key)

    async def set(self, key: str, value: str, ex: int):
        await self.client.set(key, value, ex=ex)

    async def ping(self):
        return await self.client.ping()


redis_client = RedisClient()
