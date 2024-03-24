from asyncio_redis import Connection


async def get_data(conn: Connection, key) -> dict:
    return await conn.get(key)
