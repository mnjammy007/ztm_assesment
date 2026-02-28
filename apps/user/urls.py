from rest_framework.routers import DefaultRouter
from apps.user.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from django.urls import path, include
from apps.user.serializers import CustomTokenObtainPairSerializer

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
urlpatterns = [
    # JWT
    path(
        "login/",
        TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer),
        name="login",
    ),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
