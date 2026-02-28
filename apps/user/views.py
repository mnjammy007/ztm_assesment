from rest_framework import viewsets, permissions
from apps.user.models import User
from apps.user.serializers import UserSerializer
from apps.user.permissions import IsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        # I don't want users to be able to "List" all users, I am restricting the queryset so they only see themselves.
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        if self.action == "create":
            # Allow anyone to register
            return [permissions.AllowAny()]

        # For 'update', 'partial_update', 'destroy', 'retrieve' user must be logged in AND be the owner
        return [permissions.IsAuthenticated(), IsOwner()]
