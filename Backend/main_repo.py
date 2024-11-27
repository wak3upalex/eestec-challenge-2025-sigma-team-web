from repository.user_repository import UserRepository
from repository.utils import hash_password, verify_password

def main():
    """Пример использования репозитория пользователей."""
    repo = UserRepository()

    # Создание пользователя
    email = "user@example.com"
    password = "securepassword"
    hashed = hash_password(password)

    print(f"Попытка создания пользователя с email: {email}")
    user = repo.create_user(email, hashed)
    if user:
        print(f"Создан пользователь: {user}")
    else:
        print(f"Не удалось создать пользователя с email: {email}")

    # Получение пользователя по email
    fetched_user = repo.get_user_by_email(email)
    if fetched_user:
        print(f"Получен пользователь по email: {fetched_user}")
    else:
        print(f"Пользователь с email '{email}' не найден.")

    # Проверка пароля
    if fetched_user:
        is_correct = verify_password("securepassword", fetched_user.hashed_password)
        print(f"Пароль верный: {is_correct}")

    # Обновление пароля пользователя
    if fetched_user:
        new_password = "newsecurepassword"
        new_hashed = hash_password(new_password)
        updated_user = repo.update_user(fetched_user.id, hashed_password=new_hashed)
        if updated_user:
            print(f"Обновленный пользователь: {updated_user}")
        else:
            print(f"Не удалось обновить пользователя с ID: {fetched_user.id}")

        # Проверка нового пароля
        if updated_user:
            is_correct_new = verify_password("newsecurepassword", updated_user.hashed_password)
            print(f"Новый пароль верный: {is_correct_new}")

    # Получение всех пользователей
    all_users = repo.get_all_users()
    print(f"Все пользователи: {all_users}")

    # Удаление пользователя
    if fetched_user:
        success = repo.delete_user(fetched_user.id)
        print(f"Пользователь удален: {success}")

        # Проверка удаления
        deleted_user = repo.get_user_by_id(fetched_user.id)
        if not deleted_user:
            print(f"Пользователь с ID '{fetched_user.id}' успешно удален.")
        else:
            print(f"Не удалось удалить пользователя с ID '{fetched_user.id}'.")

if __name__ == "__main__":
    main()
