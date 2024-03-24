import aio_pika
from rabbit.queue.create import CreateQueue
from db.connect_info.get.get import get_connection_info
from conf.config import RabbitMQ
from loguru import logger
class Consumer:
    def __init__(self):
        self.queues = []
        self.queue_creator = CreateQueue()

    def consume(self, message: aio_pika.Message):
        pass

    async def get_queues_name(self):
        connections_info = await get_connection_info()
        queues = []
        for con_info in connections_info:
            queues.append(self.queue_creator.create_queue_name(con_info))
        return queues

    async def create_queue(self):
        connection = await aio_pika.connect_robust(RabbitMQ.BROKER_URL)
        channel = await connection.channel()
        names_collection = await self.get_queues_name()
        for names in names_collection:
            for name in names:
                self.queues.append(await channel.get_queue(name))

    async def callback(self, message: aio_pika.Message):
        logger.debug("Received message: {}".format(message.body.decode()))

    async def start(self):
        await self.create_queue()
        for queue in self.queues:
            await queue.consume(self.callback)
