from typing import List, Optional
from peewee import IntegrityError

from domain.models import User
from domain.repositories import UserRepositoryInterface
from repository.database import db
from repository.migrations import UserModel
from repository.utils import hash_password, verify_password

class UserRepository(UserRepositoryInterface):
    def __init__(self):
        if db.is_closed():
            db.connect()
        db.create_tables([UserModel], safe=True)
    def create_user(self, email: str, hashed_password: str) -> Optional[User]:
        try:
            user = UserModel.create(email=email, hashed_password=hashed_password)
            return User(id=user.id, email=user.email, hashed_password=user.hashed_password)
        except IntegrityError:
            # Логирование ошибки или обработка дубликата
            print(f"Пользователь с email '{email}' уже существует.")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        try:
            user = UserModel.get(UserModel.id == user_id)
            return User(id=user.id, email=user.email, hashed_password=user.hashed_password)
        except UserModel.DoesNotExist:
            return None
    def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            user = UserModel.get(UserModel.email == email)
            return User(id=user.id, email=user.email, hashed_password=user.hashed_password)
        except UserModel.DoesNotExist:
            return None

    def get_all_users(self) -> List[User]:
        users = UserModel.select()
        return [User(id=user.id, email=user.email, hashed_password=user.hashed_password) for user in users]

    def update_user(self, user_id: int, email: Optional[str] = None, hashed_password: Optional[str] = None) -> Optional[User]:
          fields = {}
          if email is not None:
              fields['email'] = email
          if hashed_password is not None:
              fields['hashed_password'] = hashed_password
  
          if not fields:
              return self.get_user_by_id(user_id)
  
          try:
              query = UserModel.update(**fields).where(UserModel.id == user_id)
              rows_updated = query.execute()
              if rows_updated:
                  return self.get_user_by_id(user_id)
              return None
          except IntegrityError:
              print(f"Не удалось обновить пользователя с ID '{user_id}'. Возможно, email '{email}' уже используется.")
              return None

      def delete_user(self, user_id: int) -> bool:
          rows_deleted = UserModel.delete().where(UserModel.id == user_id).execute()
          return rows_deleted > 0

      def __del__(self):
          if not db.is_closed():
              db.close()
