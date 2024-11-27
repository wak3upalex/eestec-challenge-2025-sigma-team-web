from peewee import Model, CharField

from repository.database import db


class UserModel(Model):
    email = CharField(unique=True)
    hashed_password = CharField()

    class Meta:
        database = db
        table_name = 'users'


def migrate():
    with db:
        db.create_tables([UserModel])
