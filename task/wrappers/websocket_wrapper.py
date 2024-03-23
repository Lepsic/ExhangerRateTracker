import websockets
from websockets import WebSocketClientProtocol
import aio_pika
from task.binance.base import BinanceTaskBase
from task.wrappers.base import BaseWrapper
from task.binance.task import BinanceTask
from loguru import logger
import asyncio


class TaskWrapper(BaseWrapper):

    def __init__(self, *args, **kwargs):
        super(TaskWrapper, self).__init__()
        self.task_list = self.create_task_classes()

    async def task(self, instance: BinanceTaskBase, ws: WebSocketClientProtocol, channel, routing_key: str):
        """Queue - очередь на брокере"""
        recconnect_count = 0
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
            recconnect_count += 1
            logger.warning(f"Reconnecting \n try {recconnect_count}")
            ws = await instance.connection()
            await self.task(instance=instance, ws=ws, channel=channel, routing_key=routing_key)
            logger.warning(f"Reconnecting try {recconnect_count} failed")
            if recconnect_count == 10:
                logger.critical(f"Reconnecting failed raise Exception {error}")
                raise Exception(f"Reconnecting error")
        except Exception as error:
            logger.error(f"Unknown error {error}")

    def create_task_classes(self):
        return [BinanceTask(currency_pair="BTC-USDT", url="wss://stream.binance.com:9443/ws/btcusdt@trade")]

    async def task_creation(self, *args, **kwargs) -> list:
        tasks = []
        for task in self.task_list:
            ws = await task.connection()
            tasks.append(self.task(instance=task, ws=ws, channel="test", routing_key="test"))
        return tasks

    async def task_startup(self):
        tasks = await self.task_creation()
        for task in tasks:
            await task
