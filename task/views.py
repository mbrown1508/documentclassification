from rest_framework import viewsets, mixins

from task.models import Task
from task.serializers import TaskSerializer


class TaskViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer