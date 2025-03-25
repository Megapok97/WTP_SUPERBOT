from queue import Queue
from typing import Type, TYPE_CHECKING

from PIL import Image

from app.superbot.interface import Keyboard

if TYPE_CHECKING:
    from app.superbot.event import Event


class BaseIntegration:
    name = None

    def __init__(self, events_queue: Queue, event_class: Type['Event']):
        self._events_queue = events_queue
        self._event_class = event_class

    def send_message(self, chat_id: str, message: str = None, photos: list[Image] = None, keyboard: Keyboard = None):
        raise NotImplementedError()

    def polling(self):
        raise NotImplementedError()
