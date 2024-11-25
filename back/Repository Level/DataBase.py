from peewee import *

db = SqliteDatabase('Users.db')

class Users(Model):
    adress = TextField(unique=True)
    password = TextField()

    class Meta:
        database = db # This model uses the "people.db" database.

db.create_tables([Users])

def print_last_five_artists():
    """ Печатаем последние 5 записей в таблице исполнителей"""
    print('########################################################')
    cur_query = Users.select().limit(5).order_by(Users.adress.desc())
    for item in cur_query.dicts().execute():
        print('user: ', item)

def create(adress, password):
    Users.create(adress =  adress, password = password)

def delete(adress):
    user = Users.get(Users.adress == adress)
    user.delete_instance()

def find(adress):
    return Users.get(Users.adress == adress)

db.close()