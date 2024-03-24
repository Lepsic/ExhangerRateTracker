from task.wrappers.websocket_wrapper import TaskWrapper
import asyncio
from task.coingeko.task import start




if __name__ == '__main__':
    tasks = TaskWrapper()
    asyncio.run(tasks.task_startup())


# if __name__ == '__main__':
#     asyncio.run(start())