from fastapi import FastAPI
import uvicorn
import websockets
from task.wrappers.websocket_wrapper import TaskWrapper
import asyncio
from db.db_startup import startup_database

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


@app.on_event("startup")
async def startup():
    await startup_database()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
