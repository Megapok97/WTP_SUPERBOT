from queue import Queue
from typing import Type
from PIL import Image
from vk_api import VkApi, VkUpload
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

from app.superbot.event import Event
from app.superbot.integrations.base import BaseIntegration
from app.superbot.interface import Keyboard
from app.utils import image2bytes_stream


class VkontakteIntegration(BaseIntegration):
    name = 'vkontakte'

    def __init__(self, events_queue: Queue, event_class: Type[Event], token: str):
        super(VkontakteIntegration, self).__init__(events_queue, event_class)

        self._session = VkApi(token=token)
        self._vk_api = self._session.get_api()

        self._upload_api = VkUpload(self._session)
        self._long_polling_api = VkLongPoll(self._session)

    def _convert_keyboard(self, keyboard: Keyboard) -> VkKeyboard:
        converted_keyboard = VkKeyboard()

        for index, buttons_row in enumerate(keyboard.layout):
            for button in buttons_row:
                converted_keyboard.add_button(button.text)

            if index < keyboard.height - 1:
                converted_keyboard.add_line()

        return converted_keyboard

    def send_message(self, chat_id: str, message: str = None, photos: list[Image] = None, keyboard: Keyboard = None):
        additional_kwargs = {}

        if photos is not None:
            additional_kwargs['attachment'] = []
            photo_streams = [image2bytes_stream(p) for p in photos]
            uploaded_photos = self._upload_api.photo_messages(photos=photo_streams)

            for uploaded_photo in uploaded_photos:
                photo_string = 'photo{}_{}'.format(uploaded_photo['owner_id'], uploaded_photo['id'])
                additional_kwargs['attachment'].append(photo_string)

            additional_kwargs['attachment'] = ','.join(additional_kwargs['attachment'])

        if keyboard is not None:
            additional_kwargs['keyboard'] = self._convert_keyboard(keyboard).get_keyboard()

        self._vk_api.messages.send(user_id=chat_id, message=message, random_id=get_random_id(), **additional_kwargs)

    def polling(self):
        for event in self._long_polling_api.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text is not None:
                self._events_queue.put(self._event_class(event.user_id, event.message, self))
