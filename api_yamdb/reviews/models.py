from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_USERNAME_LENGTH = 100
MAX_EMAIL_LENGTH = 100
MAX_NAME_LENGTH = 100
MAX_ROLE_LENGTH = 15


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLE_CHOICES = [
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
]

class User(AbstractUser):
    username = models.CharField(
        verbose_name='Логин',
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
    )

    email = models.EmailField(
        verbose_name='Email',
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=MAX_ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
    )

    bio = models.TextField(
        verbose_name='Инфо',
        blank=True,
    )

    first_name = models.CharField(
        verbose_name='Имя',
        max_length=MAX_NAME_LENGTH,
        blank=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=MAX_NAME_LENGTH,
        blank=True,
    )


