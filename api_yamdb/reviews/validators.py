import re

from django.conf import settings
from django.core.exceptions import ValidationError


def check_username(username):
    if username == settings.FORBIDDEN_USERNAME:
        raise ValidationError(
            f"Имя '{username}' не разрешено."
        )

    allowed_chars = settings.USERNAME_REGEX.strip('^\\Z')
    invalid_chars = re.sub(allowed_chars, '', username)

    if invalid_chars:
        raise ValidationError(
            f'Имя содержит недопустимые символы: {invalid_chars}'
        )

    return username
