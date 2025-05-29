from django.conf import settings
from rest_framework import serializers

from reviews.models import MAX_USERNAME_LENGTH, MAX_EMAIL_LENGTH, User


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=MAX_USERNAME_LENGTH
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_EMAIL_LENGTH
    )

class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_USERNAME_LENGTH,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=settings.CONFIRMATION_CODE_LENGTH,
        required=True
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)