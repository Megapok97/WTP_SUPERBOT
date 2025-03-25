from PIL import Image

from app.superbot.integrations.base import BaseIntegration
from app.superbot.interface import Keyboard


class Event:
    def __init__(self, chat_id: str, message: str, integration: BaseIntegration):
        self.chat_id = chat_id
        self.message = message
        self.integration = integration

    def reply(self, message: str = None, photos: list[Image] = None, keyboard: Keyboard = None):
        self.integration.send_message(self.chat_id, message, photos, keyboard)
