from db.connect_info.schema.get.connection_info import ConnectionInfo
import aio_pika
from conf.config import RabbitMQ
import asyncio

class CreateQueue:
    def __init__(self):
        self.queue_dict = {}

    async def create(self, connect_info: ConnectionInfo) -> list:
        connection = await aio_pika.connect_robust(RabbitMQ.BROKER_URL)
        channel = await connection.channel()
        for name in self.create_queue_name(connect_info):
            if name in self.queue_dict.keys():
                continue
            self.queue_dict.update({name: await channel.declare_queue(name, arguments=RabbitMQ.arguments)})

    def create_queue_name(self, connect_info: ConnectionInfo) -> list[str]:
        names = []
        currency_pair = self.separate(connect_info.currency_pair)
        for parsing in currency_pair[0]:
            for target in currency_pair[1]:
                names.append("/".join([parsing, target]))
        return names

    def separate(self, currency_pair: str):
        parsing, target = currency_pair.rsplit("-", 1)
        parsing = parsing.split(",")
        target = target.split(",")
        return [parsing, target]


if __name__ == "__main__":
    create_queue = CreateQueue()
    # queue.create_queue_name(connect_info=[ConnectionInfo(currency_pair="tron-usd", url="http://localhost:", id=1,
    #                                                             task_type="test", wrapper_type="test"),
    #                                              ConnectionInfo(currency_pair="bitcoin,ethereum,tether,tron-rub,usd",
    #                                                             url="http://localhost:", id=1,
    #                                                             task_type="test", wrapper_type="test")])

    asyncio.run(create_queue.create(ConnectionInfo(currency_pair="bitcoin,ethereum,tether,tron-rub,usd",
                                                        url="http://localhost:", id=1,
                                                        task_type="test", wrapper_type="test")))
    asyncio.run(create_queue.create(ConnectionInfo(currency_pair="tron-usd", url="http://localhost:", id=1,
                                                                task_type="test", wrapper_type="test")))