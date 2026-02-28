import django_filters
from apps.task.models import Task


class TaskFilter(django_filters.FilterSet):
    completed = django_filters.BooleanFilter()

    class Meta:
        model = Task
        fields = ["completed"]
