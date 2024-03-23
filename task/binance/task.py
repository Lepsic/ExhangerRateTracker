import json
from abc import ABC
import asyncio
import websockets
from websockets import WebSocketClientProtocol
from loguru import logger

from task.binance.base import BinanceTaskBase


class BinanceTask(BinanceTaskBase):
    logger.add("pars.log", rotation="500MB")

    def __init__(self, *args, **kwargs):
        super(BinanceTaskBase, self).__init__(*args, **kwargs)
        self.url = kwargs.get('url', None)

    async def connection(self) -> WebSocketClientProtocol:
        ws = await websockets.connect(self.url)
        logger.info(f"connecting to {self.url}")
        return ws

    # async def execute(self, ws: WebSocketClientProtocol) -> None:
    #     try:
    #         async with ws as websocket:
    #             await websocket.pong()
    #             data = await websocket.recv()
    #             data = json.loads(data)
    #             logger.debug(f"Price: {data.get("p")} {super().currency_pair}")
    #             return data.get("p")
    #     except websockets.WebSocketException as error:
    #         logger.warning(f"Exception occurred, trouble with connecting to websocket {self.url}, {error}")
    #         raise Exception(f"Exception occurred, trouble with connecting")

    async def execute(self, ws: WebSocketClientProtocol) -> None:
        try:
            await ws.pong()
            data = await ws.recv()
            data = json.loads(data)
            logger.debug(f"Price: {data.get("p")} {self.currency_pair}")
            return data.get("p")
        except websockets.WebSocketException as error:
            logger.warning(f"Exception occurred, trouble with connecting to websocket {self.url}, {error}")
            raise Exception(f"Exception occurred, trouble with connecting")
