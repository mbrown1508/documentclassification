from rest_framework import serializers

from task.models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    classify = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='classify-detail'
    )

    class Meta:
        model = Task
        fields = ("url", 'id', "type", "ready", "in_progress", "completed", "worker_uuid","result","created",
                    "application","classifier","document","docset","classify")
        read_only_fields = ('classifier', 'docset', 'document', 'application', 'type', 'classify', )