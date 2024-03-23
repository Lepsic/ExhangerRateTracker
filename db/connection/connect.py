import asyncpg
from loguru import logger
from conf.config import ConfigDatabase


async def connection() -> asyncpg.Connection:
    try:
        conn = await asyncpg.connect(
            user=ConfigDatabase.DB_USER,
            password=ConfigDatabase.DB_PASSWORD,
            database=ConfigDatabase.DB_NAME,
            host=ConfigDatabase.DB_HOST,
            port=ConfigDatabase.DB_PORT
        )
        return conn
    except Exception as error:
        logger.critical("Connection bd error", error)



