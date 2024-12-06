import pytest

from repository.database import db
from repository.migrations import UserModel
from repository.user_repository import UserRepository
from repository.utils import hash_password, verify_password


@pytest.mark.parametrize("real_password, entered_password", [('securepassword', 'securepassword'),
                                                             ('securepassword', 'other_password'),
                                                             ('126549', '126549'),
                                                             ('securepassword', '126549')])
def test_hashing(real_password, entered_password):
    if real_password == entered_password:
        assert verify_password(entered_password, hash_password(real_password))
    else:
        assert not (verify_password(entered_password, hash_password(real_password)))


@pytest.fixture(scope='function')
def setup_db():
    # Подключаемся к базе данных
    db.connect()
    db.create_tables([UserModel])  # Создаём таблицу User для каждого теста

    user_repository = UserRepository()

    yield user_repository
    db.drop_tables([UserModel])
    db.close()


def test_create_user(setup_db):
    user_repository = setup_db
    user = user_repository.create_user("user@example.com", hash_password("securepassword"))
    # Проверяем, что пользователь был успешно создан
    assert user.email == "user@example.com"
    assert verify_password('securepassword', user.hashed_password)

    # Проверка на попытку создать пользователя с существующим email
    with pytest.raises(ValueError):
        user_repository.create_user("user@example.com", hash_password("otherpassword"))


def test_get_user_by_email(setup_db):
    user_repository = setup_db
    user_repository.create_user("user@example.com", hash_password("securepassword"))

    # Проверяем, что можем получить пользователя по имени
    user = user_repository.get_user_by_email("user@example.com")
    assert user.email == 'user@example.com'
    assert verify_password('securepassword', user.hashed_password)


def test_get_user_by_id(setup_db):
    user_repository = setup_db
    user_repository.create_user("user@example.com", hash_password("securepassword"))

    # Проверяем, что можем получить пользователя по имени
    user = user_repository.get_user_by_id(1)
    assert user.email == 'user@example.com'
    assert verify_password('securepassword', user.hashed_password)


def test_get_all_users(setup_db):
    user_repository = setup_db
    user_repository.create_user("user@example.com", hash_password("securepassword"))
    user_repository.create_user("next@example.com", hash_password("othersecurepassword"))

    users = user_repository.get_all_users()
    assert len(users) == 2
    assert users[0].email == 'user@example.com'
    assert verify_password('securepassword', users[0].hashed_password)
    assert users[1].email == 'next@example.com'
    assert verify_password('othersecurepassword', users[1].hashed_password)


def test_update_user(setup_db):
    user_repository = setup_db
    user_repository.create_user("user1@example.com", hash_password("securepassword"))
    user_repository.create_user("user2@example.com", hash_password("securepassword"))
    user_repository.update_user(1, email="next@example.com")
    user_repository.update_user(2, hashed_password=hash_password("otherpassword"))
    user1 = user_repository.get_user_by_id(1)
    user2 = user_repository.get_user_by_id(2)
    assert user1.email == "next@example.com"
    assert verify_password('securepassword', user1.hashed_password)
    assert user2.email == "user2@example.com"
    assert verify_password('otherpassword', user2.hashed_password)

    # Проверка на попытку обновить пользователя с существующим email
    with pytest.raises(ValueError):
        user_repository.update_user(1, "user2@example.com", hash_password("anotherpassword"))


def test_delete_user(setup_db):
    user_repository = setup_db
    user_repository.create_user("user@example.com", hash_password("securepassword"))
    user_repository.create_user("next@example.com", hash_password("othersecurepassword"))
    user_repository.delete_user(1)

    assert user_repository.get_user_by_id(1) is None

    users = user_repository.get_all_users()
    assert len(users) == 1
    assert users[0].email == "next@example.com"
