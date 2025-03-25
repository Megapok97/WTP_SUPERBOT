import os
import uuid

import peewee

from app.config import ENVIRONMENT


def connect_database():
    if ENVIRONMENT == 'production':
        file_path = os.path.join(os.path.dirname(__file__), '../data/database.sqlite')
        database = peewee.SqliteDatabase(file_path)
    else:
        file_path = os.path.join(os.path.dirname(__file__), '../data/database_dev.sqlite')
        database = peewee.SqliteDatabase(file_path)
    return database


database = connect_database()


class BaseModel(peewee.Model):
    id = peewee.UUIDField(default=uuid.uuid4, primary_key=True)

    class Meta:
        database = database

    def update_one(self, **fields):
        for field, value in fields.items():
            setattr(self, field, value)
        self.save()


class User(BaseModel):
    pass


class Account(BaseModel):
    user = peewee.ForeignKeyField(User, backref='accounts')

    platform = peewee.CharField()
    platform_id = peewee.CharField()
    keyboard = peewee.CharField(null=True)

    class Meta:
        indexes = [(('platform', 'platform_id'), True)]


class Game(BaseModel):
    account = peewee.ForeignKeyField(Account, backref='games')

    status = peewee.CharField()
    pokemon_number = peewee.IntegerField()
    answer = peewee.CharField(null=True)

    start_date = peewee.DateTimeField()
    end_date = peewee.DateTimeField(null=True)


def init_database():
    database.connect()
    database.create_tables([User, Account, Game], safe=True)
    database.close()
