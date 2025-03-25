import peewee

from app.database import Account, User, Game
from app.superbot import Event as BaseEvent


class Event(BaseEvent):
    def __init__(self, *args, **kwargs):
        super(Event, self).__init__(*args, **kwargs)
        platform, platform_id = self.integration.name, self.chat_id

        try:
            self.account = Account.get(platform=platform, platform_id=platform_id)
        except peewee.DoesNotExist:
            self.account = Account.create(platform=platform, platform_id=platform_id, user=User.create())

        try:
            self.game = self.account.games.select().where(Game.status == 'active').get()
        except peewee.DoesNotExist:
            self.game = None
