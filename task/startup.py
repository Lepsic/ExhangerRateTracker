from task.wrappers.websocket_wrapper import TaskWrapper
import asyncio

if __name__ == '__main__':
    tasks = TaskWrapper()
    asyncio.run(tasks.task_startup())