from typing import List, Optional

from domain.models import User


class UserRepositoryInterface:

    def create_user(self, email: str, hashed_password: str) -> User:
        raise NotImplementedError

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    def get_all_users(self) -> List[User]:
        raise NotImplementedError

    def delete_user(self, user_id: int) -> bool:
        raise NotImplementedError
