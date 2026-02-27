from rest_framework.routers import DefaultRouter
from apps.task.views import TaskViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from django.urls import path, include

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
urlpatterns = [
    # JWT
    path(
        "login/",
        TokenObtainPairView.as_view(),
    ),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
# urlpatterns = router.urls
