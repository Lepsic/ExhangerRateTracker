from aio_pika import Message
from fastapi import FastAPI
import uvicorn
import websockets
from task.wrappers.wrapper import TaskWrapper
import asyncio
from db.db_startup import startup_database
import aio_pika
from loguru import logger
from  rabbit.consumer.consumer import Consumer

app = FastAPI()


# @app.get("/")
# async def connect_to_binance_ws():
#     async with websockets.connect('wss://stream.binance.com:9443/ws/btcusdt@trade') as websocket:
#         while True:
#             data = await websocket.recv()
#             print(data)

@app.get("/")
async def index():
    return {"message": "hello"}


async def consume(message: aio_pika.Message):
    async with message.process():
        print(message.body)



@app.on_event("startup")
async def startup():
    consumer = Consumer()
    await consumer.start()
    # connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    # channel = await connection.channel()
    # queue = await channel.get_queue("bitcoin/rub")
    # queue1 = await channel.get_queue("bitcoin/usd")
    # await queue.consume(callback=consume)
    # await queue1.consume(callback=consume)





if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
