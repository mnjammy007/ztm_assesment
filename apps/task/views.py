from rest_framework import viewsets
from apps.task.models import Task
from apps.task.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from apps.task.filters import TaskFilter
from apps.shared.permissions import IsOwnerOrAdmin


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()

        user = self.request.user

        # Superuser or Admin can see all tasks
        if user.is_superuser or user.is_staff:
            return Task.objects.all()

        return Task.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
