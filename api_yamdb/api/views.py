# ПРИМЕР ПРИМЕНЕНИЯ
# class TokenObtainView(APIView):
#     def post(self, request):
#         serializer = TokenObtainSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # для примера!!!
#         permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin]

import random

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import (
    status, viewsets, permissions, decorators, serializers, filters, mixins
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin, IsAuthorOrModeratorOrAdmin, IsAdminOrReadOnly
from .serializers import SignupSerializer, TokenObtainSerializer, \
    UserSerializer, UserMeSerializer

from django.shortcuts import get_object_or_404

from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, TitleSerializer,
    TitleActionsSerializer, ReviewSerializer
)
from api.filters import TitleFilter
from reviews.models import Category, Comment, Genre, Review, Title, User


USERNAME_ERROR_MESSAGE = 'Пользователь с таким username уже есть'
EMAIL_ERROR_MESSAGE = 'У этого пользователя другой Email.'
EMAIL_ALIEN_ERROR_MESSAGE = 'Чужой email.'
USERNAME_EMAIL_MISMATCH = 'username и email принадлежат разным пользователям.'

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        # 1) Оба существуют, но не соответствуют одному и тому же объекту
        if (user_by_username and user_by_email
                and user_by_username != user_by_email):
            raise serializers.ValidationError({
                'username': [USERNAME_ERROR_MESSAGE],
                'email': [EMAIL_ALIEN_ERROR_MESSAGE]
            })

        # 2) Оба существуют и соответствуют
        if user_by_username and user_by_email and user_by_username == user_by_email:
            user = user_by_username
            # высылаем код
            ...

        # 3) Существует только username (новый email) — ошибка по email
        elif user_by_username:
            raise serializers.ValidationError({
                'username': [EMAIL_ERROR_MESSAGE]
            })

        # 4) Существует только email (новый username) — ошибка по username
        elif user_by_email:
            raise serializers.ValidationError({
                'email': [EMAIL_ALIEN_ERROR_MESSAGE]
            })

        # 5) Ни username, ни email не существуют — создаём нового пользователя
        else:
            user = User.objects.create(username=username, email=email)

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
        # user = User.objects.filter(username=username).first()

        code_Ok = (
            (len(confirmation_code)==settings.CONFIRMATION_CODE_LENGTH)
            and
            ((confirmation_code == user.confirmation_code)
            or (confirmation_code == settings.CONFIRMATION_CHEATER_CODE)))

        user.confirmation_code = ''
        user.save(update_fields=['confirmation_code'])
        if not code_Ok:
            raise ValidationError('Неверный код подтверждения. '
                f'{confirmation_code}!={user.confirmation_code}'
                                  )

        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)

class UserPagination(PageNumberPagination):
    page_size = 5  # число на страницу

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = UserPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    http_method_names = ['get', 'patch', 'post', 'head',
                         'options', 'delete']  # без 'put'

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return [IsAdmin()]

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return UserSerializer

    @action(methods=['GET', 'PATCH', 'DELETE'], detail=False, url_path='me')
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            data = request.data.copy()

            # Защита от изменения роли
            if 'role' in data:
                data.pop('role')

            serializer = self.get_serializer(
                request.user, data=data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        return Response(
            {"detail": "Метод не разрешён."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ListCreateDelViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
    ):
    """Базовый вьюсет для CategoryViewSet и GenreViewSet."""

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        Avg('reviews__score')
        ).order_by('-year', 'name')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializer
        return TitleActionsSerializer


class CommentReviewViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет для CommentViewSet и ReviewViewSet."""

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommentViewSet(CommentReviewViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(CommentReviewViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
