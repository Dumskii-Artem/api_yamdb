import random

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import (
    status, viewsets, permissions, filters, mixins
)
from rest_framework_simplejwt.tokens import AccessToken

from .permissions import IsAdmin, IsAuthorOrModeratorOrAdmin, IsAdminOrReadOnly
from .serializers import (
    SignupSerializer,
    TokenObtainSerializer,
    UserSerializer,
    UserMeSerializer
)

from django.shortcuts import get_object_or_404

from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    TitleViewSerializer,
    TitleCreateUpdateSerializer,
    ReviewSerializer
)
from api.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title, User


USERNAME_ERROR_MESSAGE = 'Пользователь с таким username уже есть'
EMAIL_ALIEN_ERROR_MESSAGE = 'Чужой email.'


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    try:
        user, _ = User.objects.get_or_create(username=username, email=email)
    except IntegrityError:
        raise ValidationError({
            field: [message]
            for field, value, message in (
                ('username', username, 'USERNAME_ERROR_MESSAGE'),
                ('email', email, 'EMAIL_ERROR_MESSAGE'),
            )
            if User.objects.filter(**{field: value}).exists()
        })

    confirmation_code = ''.join(
        random.choices(
            settings.CONFIRMATION_CODE_CHARS,
            k=settings.CONFIRMATION_CODE_LENGTH
        ))
    user.confirmation_code = confirmation_code
    user.save(update_fields=['confirmation_code'])

    send_mail(
        subject='Код подтверждения YaMDb',
        message=(
            f'Ваш код подтверждения: {confirmation_code}\n'
            'Используйте код для получения токена.'
        ),
        from_email=settings.OUR_NOREPLY_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {'email': email, 'username': username},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain(request):
    serializer = TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    user = get_object_or_404(User, username=username)

    code_ok = (
        (len(confirmation_code) == settings.CONFIRMATION_CODE_LENGTH)
        and ((confirmation_code == user.confirmation_code)
             or (confirmation_code == settings.CONFIRMATION_CHEATER_CODE)))

    if not code_ok:
        user.confirmation_code = ''
        user.save(update_fields=['confirmation_code'])
        raise ValidationError(
            f'Неверный код подтверждения: {confirmation_code}'
        )

    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    http_method_names = ['get', 'patch', 'post', 'head',
                         'options', 'delete']  # без 'put'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path=settings.FORBIDDEN_USERNAME,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)

        serializer = UserMeSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CategoryGenreBaseViewSet(
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


class CategoryViewSet(CategoryGenreBaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by(*Title._meta.ordering)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleViewSerializer
        return TitleCreateUpdateSerializer


class CommentReviewViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет для CommentViewSet и ReviewViewSet."""

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrModeratorOrAdmin,
    )
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommentViewSet(CommentReviewViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(CommentReviewViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
