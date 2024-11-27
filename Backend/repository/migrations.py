from peewee import Model, CharField
from repository.database import db

class User(Model):
    def __init__(self,e_mail, password):
        e_mail = CharField(unique=True)
        self.password = CharField()

      class Meta:
        database = db
        table_name = 'users'

def migrate():
    with db:
        db.create_tables([UserModel])
