import os
from enum import Enum, unique

from peewee import Model, IntegerField, PostgresqlDatabase, TextField
from urllib3.util import parse_url

db_url = parse_url(os.getenv('DATABASE_URL'))

# Берём из auth имя пользователя и пароль от БД
username, password = db_url.auth.split(':')

database = PostgresqlDatabase(
    db_url.path[1:],  # Пропускаем первый "/", так как он не является названием БД
    host=db_url.host,
    user=username,
    password=password
)


class BaseModel(Model):
    class Meta:
        database = database


@unique
class UserState(Enum):
    authorizing = 1
    base = 2
    integrating_tg = 3
    integrating_vk = 4
    trading = 5

    @classmethod
    def as_choices(cls):
        return [reversed(item) for item in cls.__members__.items()]


class User(BaseModel):
    tg_id = IntegerField(null=True, unique=True, help_text='Telegram User Id')
    vk_id = IntegerField(null=True, unique=True, help_text='VK User Id')
    state = IntegerField(default=UserState.authorizing, choices=UserState.as_choices())
    additional_parameter = TextField()


def create_tables():
    with database:
        database.create_tables([User])
