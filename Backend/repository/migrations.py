from peewee import Model, CharField

from repository.database import db


class BaseModel(Model):
    class Meta:
        database = db
        table_name = 'users'

class UserModel(BaseModel):
    email = CharField(unique=True)
    hashed_password = CharField()

        





def migrate():
    with db:
        db.create_tables([UserModel])
