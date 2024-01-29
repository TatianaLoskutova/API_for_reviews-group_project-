from django.contrib.auth.models import AbstractUser
from django.db import models

from .constants import LITTLE_LENGTH, BIG_LENGTH


class CustomUser(AbstractUser):
    """
    Модель кастомного пользователя.
    """

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        'Email',
        unique=True,
        blank=False,
        max_length=BIG_LENGTH
    )
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        choices=Role.choices, default=Role.USER,
        blank=True,
        max_length=LITTLE_LENGTH,
    )
    confirmation_code = models.CharField(
        'confirmation code',
        max_length=LITTLE_LENGTH, blank=True, null=True,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.role
