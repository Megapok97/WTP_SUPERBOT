from queue import Queue
from typing import Type

import telebot
from PIL import Image
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.superbot.event import Event
from app.superbot.integrations.base import BaseIntegration
from app.superbot.interface import Keyboard
from app.utils import image2bytes_stream


class TelegramIntegration(BaseIntegration):
    name = 'telegram'

    def __init__(self, events_queue: Queue, event_class: Type[Event], token: str):
        super(TelegramIntegration, self).__init__(events_queue, event_class)

        self._bot = telebot.TeleBot(token, threaded=False)
        self._bot.message_handler()(self._process_message)

    def _process_message(self, message: Message):
        self._events_queue.put(self._event_class(message.json['chat']['id'], message.json['text'], self))

    def _convert_keyboard(self, keyboard: Keyboard) -> ReplyKeyboardMarkup:
        converted_keyboard = ReplyKeyboardMarkup(row_width=keyboard.width, resize_keyboard=True)

        for buttons_row in keyboard.layout:
            converted_keyboard.add(*[KeyboardButton(b.text) for b in buttons_row])

        return converted_keyboard

    def send_message(self, chat_id: str, message: str = None, photos: list[Image] = None, keyboard: Keyboard = None):
        converted_keyboard = None if keyboard is None else self._convert_keyboard(keyboard)

        if message is not None:
            self._bot.send_message(chat_id, message, reply_markup=converted_keyboard)

        for photo in photos or []:
            reply_markup = converted_keyboard if message is None else None
            self._bot.send_photo(chat_id, image2bytes_stream(photo), reply_markup=reply_markup)

    def polling(self):
        self._bot.polling()
