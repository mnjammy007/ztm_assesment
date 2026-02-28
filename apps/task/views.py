from rest_framework import viewsets
from apps.task.models import Task
from apps.task.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from apps.task.filters import TaskFilter


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
