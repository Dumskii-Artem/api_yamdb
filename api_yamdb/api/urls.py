from django.contrib.auth.views import LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import SignupView, TokenObtainView, UserViewSet

router1 = DefaultRouter()
router1.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token_obtain'),
    path('', include(router1.urls)),
]