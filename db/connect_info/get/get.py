from db.connect_info.schema.get.connection_info import ConnectionInfo
from conf.config import ConfigDatabase
from db.connection.connect import connection


async def get_connection_info():
    query = f"""SELECT id, url, currency_pair, task_type, wrapper_type FROM {ConfigDatabase.CONNECT_INFO_FIELD}"""
    conn = await connection()
    res = await conn.fetch(query)
    instance_list = []
    for instance_data in res:
        instance_list.append(ConnectionInfo(**instance_data))
    return instance_list

