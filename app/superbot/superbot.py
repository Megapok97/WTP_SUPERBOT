import queue
import time
from functools import wraps
from logging import Logger
from threading import Thread
from typing import Union, Callable, Any, Iterable, Type

from app.logger import logger
from app.superbot import Event, SkipHandler
from app.superbot.integrations.telegram import TelegramIntegration
from app.superbot.integrations.vkontakte import VkontakteIntegration


class SafeThread(Thread):
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.pop('logger')
        super(SafeThread, self).__init__(*args, **kwargs)

    def run(self) -> None:
        while True:
            try:
                self._target(*self._args, **self._kwargs)
            except Exception as exception:
                self.logger.warning(exception, exc_info=True)

            time.sleep(1)


class Superbot:
    _integrations_map = {
        'telegram': TelegramIntegration,
        'vkontakte': VkontakteIntegration,
    }

    def __init__(self, integrations: dict, concurrency: int, logger: Logger, event_class: Type[Event] = Event):
        self._integration_options = integrations
        self._concurrency = concurrency
        self._logger = logger
        self._event_class = event_class

        self._events_queue = queue.Queue()
        self._integrations = {}
        self._handlers = []
        self._worker_threads = []
        self._integration_threads = []

        for _ in range(concurrency):
            self._worker_threads.append(SafeThread(target=self._process_worker, logger=self._logger))

        for integration_name, options in self._integration_options.items():
            integration_class = self._integrations_map[integration_name]
            self._integrations[integration_name] = integration_class(self._events_queue, self._event_class, **options)

            thread_target = self._integrations[integration_name].polling
            self._integration_threads.append(SafeThread(target=thread_target, logger=self._logger))

    def _process_worker(self):
        while True:
            try:
                self._process_event(self._events_queue.get_nowait())
            except queue.Empty:
                pass
            except Exception as exception:
                logger.warning(exception, exc_info=True)

            time.sleep(1)

    def _process_event(self, event: Event):
        for handler, message, message_ne in self._handlers:
            messages = message if isinstance(message, Iterable) else [message]
            messages_ne = message_ne if isinstance(message_ne, Iterable) else [message_ne]

            messages = [m.lower() for m in messages if m is not None]
            messages_ne = [m.lower() for m in messages_ne if m is not None]

            if messages and event.message.lower() not in messages:
                continue

            if messages_ne and event.message.lower() in messages_ne:
                continue

            try:
                handler(event)
            except SkipHandler:
                pass
            else:
                return

    def register_handler(self, handler: Callable, message: Union[Iterable[str], str] = None,
                         message_ne: Union[Iterable[str], str] = None):
        self._handlers.append((handler, message, message_ne))

    def message_handler(self, message: Union[Iterable[str], str] = None,
                        message_ne: Union[Iterable[str], str] = None) -> Callable:
        def decorator(function: Callable) -> Callable:
            self.register_handler(function, message, message_ne)

            @wraps(function)
            def wrapper(*args, **kwargs) -> Any:
                return function(*args, **kwargs)

            return wrapper

        return decorator

    def start(self):
        for thread in self._integration_threads + self._worker_threads:
            thread.start()

        for thread in self._integration_threads + self._worker_threads:
            thread.join()
