import re

from django.conf import settings
from django.core.exceptions import ValidationError


def check_username(username):
    if username == settings.FORBIDDEN_USERNAME:
        raise ValidationError(
            f"Имя '{username}' не разрешено."
        )

    if invalid_chars := re.sub(
            settings.USERNAME_REGEX.strip('^\\Z'),
            '',
            username):
        raise ValidationError(
            'Имя содержит недопустимые символы: '
            f'{"".join(sorted(set(invalid_chars)))}'
        )

    return username
