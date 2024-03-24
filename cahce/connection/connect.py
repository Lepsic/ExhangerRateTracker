import asyncio_redis
from conf.config import ReddisCache
async def connection():
    r = await asyncio_redis.Connection.create(ReddisCache.REDIS_URL, int(ReddisCache.REDIS_PORT))
    return r

