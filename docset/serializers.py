from rest_framework import serializers
from docset.models import DocSet

from application.models import Application
from task.models import Task

class DocSetSerializer(serializers.HyperlinkedModelSerializer):
    application_id = serializers.IntegerField()
    task_uuid = serializers.ReadOnlyField(source='task.uuid')
    task = serializers.HyperlinkedRelatedField(read_only=True,  view_name='task-detail')

    class Meta:
        model = DocSet
        fields = ('url', 'id', 'name', 'train_percentage', 'test_percentage',
                  'application_id', 'application', 'task_uuid', 'task')
        read_only_fields = ('application',)

    def create(self, validated_data):
        docset = super(DocSetSerializer, self).create(validated_data)
        application = Application.objects.filter(id=validated_data['application_id']).first()

        # Create a task to finish the work
        task=Task()
        task.type = 'createdocset'
        task.application = application
        task.docset = docset
        task.save()

        return docset

    def validate_application_id(self, value):
        if not Application.objects.filter(id=value).exists():
            raise serializers.ValidationError('{} is not a valid application id.'.format(value))
        return value