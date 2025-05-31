import re

from django.conf import settings
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

# FORBIDDEN_USERNAMES = ['me',]


def check_username(username):
    if username.upper() in (
            name.upper()
            for name in settings.FORBIDDEN_USERNAMES
    ):
        raise ValidationError(
            f"Имя '{username}' не разрешено."
        )

    match = re.match(
        r'^\^\[([^\]]+)\]\+\\Z$',
        settings.USERNAME_REGEX
    )

    if not match:
        raise ValueError(
            'USERNAME_REGEX не соответствует ожидаемому формату')

    wrong_chars = re.findall(rf'[^{match.group(1)}]', username)

    if wrong_chars:
        raise ValidationError(
            'Имя содержит недопустимые символы: '
            f'{", ".join(sorted(set(wrong_chars)))}'
        )


class UsernameValidator:
    def validate_username(self, value):
        check_username(value)
        return value


class RegirteredUsernameValidator:
    def validate_username(self, value):
        from reviews.models import User
        # get_object_or_404(User, username=value)
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь не найден.')

        check_username(value)
        return value
