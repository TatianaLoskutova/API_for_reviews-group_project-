from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """
    Валидатор корректного года.
    """

    now = timezone.now().year
    if value > now:
        raise ValidationError(
            'Год выпуска не может быть больше текущего года!'
        )
