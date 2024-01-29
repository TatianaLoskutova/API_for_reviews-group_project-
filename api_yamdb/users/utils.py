import random
import string


def generate_confirmation_code(email):
    """
    Рандомная генерация подтверждающего кода для регистрации пользователя.
    Без сохранения кода в БД.
    """
    confirmation_code = ''.join(
        random.choices(string.ascii_letters + string.digits, k=6)
    )
    return confirmation_code
