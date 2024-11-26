from peewee import *

db = SqliteDatabase('Users.db')

class User(Model):
    e-mail = TextField(unique=True)
    hash_password = TextField()

    class Meta:
        database = db # This model uses the "people.db" database.

def log_in(e-mail, password):
    try:
        Users.create(adress =  adress, password = password)
    except Exception as e:
        return e

def delete_user(e-mail):
    try:
        user = Users.get(Users.adress == e-mail)
        user.delete_instance()
    except Exception as e:
        return e

def sign_in(e-mail, password):
    return Users.get(Users.adress == e-mail)

db.close()
