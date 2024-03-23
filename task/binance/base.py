from task.base.base import BaseTask
from abc import abstractmethod
import websockets


class BinanceTaskBase(BaseTask):

    def __init__(self, *args, **kwargs):
        super(BaseTask, self).__init__(*args, **kwargs)

    @abstractmethod
    async def connection(self) -> websockets.connect:
        """Подключение к сокету"""

