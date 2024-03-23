from db.connection.connect import connection
from loguru import logger
from asyncpg import Connection
from conf.config import ConfigDatabase

async def startup_database():
    try:
        query = f"""
        CREATE TABLE IF NOT EXISTS public.{ConfigDatabase.CONNECT_INFO_FIELD}
(
    id SERIAL PRIMARY KEY,
    url text COLLATE pg_catalog."default" NOT NULL,
    currency_pair text COLLATE pg_catalog."default" NOT NULL,
    task_type text COLLATE pg_catalog."default" NOT NULL,
    wrapper_type text COLLATE pg_catalog."default" NOT NULL
);
    """
        insert_query = f"""
        INSERT INTO public.{ConfigDatabase.CONNECT_INFO_FIELD} (
            url, currency_pair, task_type, wrapper_type) VALUES (
            'wss://stream.binance.com:9443/ws/btcusdt@trade', 'BTC-USDT', 
            'task.binance.task.BinanceTask', 'websocket');
        INSERT INTO public.trade_info (
            url, currency_pair, task_type, wrapper_type) VALUES (
            'wss://stream.binance.com:9443/ws/ethusdt@trade', 'ETH-USDT', 
            'task.binance.task.BinanceTask', 'websocket');

        """

        conn = await connection()
        if await __check_exist_table(conn):
            return

        await conn.execute(query)
        await conn.execute(insert_query)
        logger.info("Database create insert successful")
        await conn.close()
    except Exception as error:
        logger.error(f"Trouble with execute query {error}")


async def __check_exist_table(conn: Connection):
    check = await conn.fetch(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables "
                             "WHERE table_name = {ConfigDatabase.CONNECT_INFO_FIELD})")
    check = check[0]["exists"]
    return check
