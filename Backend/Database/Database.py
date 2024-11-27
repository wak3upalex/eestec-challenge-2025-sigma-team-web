from peewee import *
import bcrypt
from abc import ABC, abstractmethod
from typing import List, TypeVar

T = TypeVar('T')


mysql_db = MySQLDatabase('users')


class DBase(ABC):
    
    @abstractmethod
    def log_in(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete_user(self, e_mail: str) -> None:
        pass

    @abstractmethod
    def sign_in(self, e_mail: str, entered_password: str) -> T:
        pass

    class Meta:
             database = mysql_db    

class User:
    def __init__(self,e_mail, password):
        self.e_mail = e_mail
        self.password = password

class UserRepository(DBase):
    e_mail = TextField(unique=True)
    hash_password = TextField()

    class Meta:
        database = mysql_db # This model uses the "people.db" database.

    def log_in(self, user: User) -> None:
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(
            password= user.password,
            salt=salt
        )
        try:
            UserRepository.create(e_mail =  user.e_mail, hash_password = hash_password)
        except Exception as e:
            return e

    def delete_user(self, e_mail: str) -> None:
        try:
            user = UserRepository.get(UserRepository.e_mail == e_mail)
            user.delete_instance()
        except Exception as e:
            return e

    def sign_in(self, e_mail, entered_password) -> User:
        try:
            user_password = UserRepository.get(UserRepository.e_mail == e_mail).password
            check = bcrypt.checkpw(
                password=entered_password,
                hashed_password=user_password
            )
            return check
        except Exception as e:
            return e
