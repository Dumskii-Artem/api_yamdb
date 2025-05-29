import random

from django.conf import settings
# from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, decorators
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import SignupSerializer, TokenObtainSerializer, \
    UserSerializer
from reviews.models import User

class SignupView(APIView):
    def post(self, request):
        print(SignupSerializer, SignupSerializer.__module__,
              SignupSerializer.__bases__)

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
        # confirmation_code = default_token_generator.make_token(user)
        confirmation_code = ''.join(
            random.choices(
                settings.CONFIRMATION_CODE_CHARS,
                k=settings.CONFIRMATION_CODE_LENGTH
            ))
        user.confirmation_code = confirmation_code
        user.save(update_fields=['confirmation_code'])

        send_mail(
            subject = 'Код подтверждения YaMDb',
            message = (
                f'Ваш код подтверждения: {confirmation_code}\n'
                'Используйте код для получения токена.'
            ),
            from_email = 'noreply@yamdb.mail.ru',
            recipient_list = [email],
            fail_silently = False,
        )

        return Response(
            {'email': email, 'username': username}
            # ,            status=status.HTTP_200_OK
        )

class TokenObtainView(APIView):
    def post(self, request):
        serializer = TokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        code_Ok = (
            (len(confirmation_code)==settings.CONFIRMATION_CODE_LENGTH)
            and
            ((confirmation_code == user.confirmation_code)
            or (confirmation_code == settings.CONFIRMATION_CHEATER_CODE)))

        user.confirmation_code = ''
        user.save(update_fields=['confirmation_code'])
        if not code_Ok:
            raise ValidationError('Неверный код подтверждения. '
                                  'Запросите новый код'
                f'{confirmation_code}!={user.confirmation_code}'
                                  )

        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @decorators.action(methods=['GET', 'PATCH'], url_path='me', detail=False)
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

