from peewee import *
import bcrypt

db = SqliteDatabase('Users.db')

class User(Model):
    e-mail = TextField(unique=True)
    hash_password = TextField()

    class Meta:
        database = db # This model uses the "people.db" database.

def log_in(e-mail, password):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(
        password=my_password,
        salt=salt
    )
    try:
        Users.create(adress =  adress, hash_password = hash_password)
    except Exception as e:
        return e

def delete_user(e-mail):
    try:
        user = Users.get(Users.adress == e-mail)
        user.delete_instance()
    except Exception as e:
        return e

def sign_in(e-mail, entered_password):
    try:
        user_password = Users.get(Users.adress == e-mail).password
        check = bcrypt.checkpw(
            password=entered_password,
            hashed_password=user_password
        )
        return check
    except Exception as e:
        return e

db.close()
