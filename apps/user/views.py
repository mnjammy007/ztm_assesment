from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.user.models import User
from apps.user.serializers import UserSerializer
from apps.shared.permissions import IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        # Superuser(we can it for admin panel) or Admin can see all users
        if user.is_superuser or user.is_staff:
            return User.objects.all()

        # I don't want users to be able to "List" all users, I am restricting the queryset so they only see themselves.
        return User.objects.filter(id=user.id)

    def get_permissions(self):
        if self.action == "create":
            # Allow anyone to register
            return [AllowAny()]

        # For 'update', 'partial_update', 'destroy', 'retrieve' user must be logged in AND be the owner/Superuser/Admin
        return [IsAuthenticated(), IsOwnerOrAdmin()]
