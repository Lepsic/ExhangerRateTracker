import websockets
from websockets import WebSocketClientProtocol
from task.wrappers.base import BaseWrapper
from loguru import logger
import asyncio
from db.connect_info.get.get import get_connection_info
from db.connect_info.schema.get.connection_info import ConnectionInfo
from task.base.base import BaseTask
from importlib import import_module
from task.ws_task.base import WebSocketTaskBase

class TaskWrapper(BaseWrapper):

    def __init__(self, *args, **kwargs):
        super(TaskWrapper, self).__init__()

    async def task(self, instance: BaseTask, ws: WebSocketClientProtocol, channel: str, routing_key: str):
        """Queue - очередь на брокере"""
        reconnect_count = 0
        try:
            while True:
                price = await instance.execute(ws=ws)
                price = str(price)
                # await channel.default_exchange.publish(
                #     aio_pika.Message(body=price),
                #     routing_key='my_queue'
                # )
                await asyncio.sleep(3)
        except websockets.exceptions.WebSocketException as error:
            reconnect_count += 1
            logger.warning(f"Reconnecting \n try {reconnect_count}")
            ws = await instance.connection()
            await self.task(instance=instance, ws=ws, channel=channel, routing_key=routing_key)
            logger.warning(f"Reconnecting try {reconnect_count} failed")
            if reconnect_count == 10:
                logger.critical(f"Reconnecting failed raise Exception {error}")
                raise Exception(f"Reconnecting error")
        except Exception as error:
            logger.error(f"Unknown error {error}")

    async def create_task_classes(self) -> list[BaseTask]:
        instances = await self.preproccess()
        tasks = []
        for instance in instances:
            task = self.get_class_instance(instance.task_type)
            task_instance = task(url=instance.url, currency_pair=instance.currency_pair, channel="test",
                                 routing_key="test")
            tasks.append(task_instance)
        return tasks

        # return [BinanceTask(currency_pair="BTC-USDT", url="wss://stream.binance.com:9443/ws/btcusdt@trade")]

    async def task_creation(self, *args, **kwargs) -> list:
        tasks = []
        for task in await self.create_task_classes():
            if isinstance(task, WebSocketTaskBase):
                ws = await task.connection()
                tasks.append(self.task(instance=task, ws=ws, channel="test", routing_key="test"))
        return tasks

    async def task_startup(self):
        tasks = await self.task_creation()
        await asyncio.gather(*tasks)

    async def preproccess(self) -> list[ConnectionInfo]:
        instances = await get_connection_info()
        return instances

    @classmethod
    def get_class_instance(cls, path: str) -> object:
        module_name, class_name = path.rsplit(":", 1)
        module = import_module(module_name)
        return getattr(module, class_name)
