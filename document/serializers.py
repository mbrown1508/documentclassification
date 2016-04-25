from rest_framework import serializers
from document.models import Document
from task.models import Task

from application.models import Application



class BaseDocumentSerializer(serializers.HyperlinkedModelSerializer):
    application_id = serializers.IntegerField()

    def create(self, validated_data):
        self.check_input(validated_data)
        return super(BaseDocumentSerializer, self).create(validated_data)

    def validate_application_id(self, value):
        if not Application.objects.filter(id=value).exists():
            raise serializers.ValidationError('{} is not a valid application id.'.format(value))
        return value

    def check_input(self, validated_data):
        if 'ocr_result' in validated_data and 'string' in validated_data:
            if validated_data['ocr_result'] is None and validated_data['string'] is None:
                raise serializers.ValidationError('ocr_result or string must be assigned a value.')
            elif validated_data['ocr_result'] is not None and validated_data['string'] is not None:
                raise serializers.ValidationError('Both ocr_result and string cannot be set.')
        elif 'ocr_result' not in validated_data and 'string' not in validated_data:
            raise serializers.ValidationError('ocr_result or string must be assigned a value.')
        else:
            if 'ocr_result' in validated_data and validated_data['ocr_result'] is None:
                raise serializers.ValidationError('ocr_result or string must be assigned a value.')
            elif 'string' in validated_data and validated_data['string'] is None:
                raise serializers.ValidationError('ocr_result or string must be assigned a value.')


    def create_task(self, type, application, document):
        task=Task()
        task.type = type
        task.application = application
        if type == 'createdocument':
            task.document = document
        elif type == 'classifydocument':
            task.classify = document
        else:
            raise Exception('Not a valid task type.')
        task.save()


class DocumentSerializer(BaseDocumentSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='document-detail')
    task_uuid = serializers.ReadOnlyField(source='documenttask.uuid')
    documenttask = serializers.HyperlinkedRelatedField(read_only=True,  view_name='task-detail')
    task = documenttask

    class Meta:
        model = Document
        fields = ('url', 'id', 'filename', 'ocr_result', 'string', 'doc_type',
                  'sub_doc_type',
                  'application_id', 'application', 'task_uuid', 'documenttask', 'task')
        read_only_fields = ('application',)
        extra_kwargs = {
            'classification': {
                'required': False,
            },
            'confidence': {
                'required': False,
            },
        }

    def create(self, validated_data):
        document = super(DocumentSerializer, self).create(validated_data)
        application = Application.objects.filter(id=validated_data['application_id']).first()
        self.create_task('createdocument', application, document)
        return document


class ClassifySerializer(BaseDocumentSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='classify-detail')
    task_uuid = serializers.ReadOnlyField(source='classifytask.uuid')
    classifytask = serializers.HyperlinkedRelatedField(read_only=True,  view_name='task-detail')
    task = classifytask

    class Meta:
        model = Document
        fields = ('url', 'filename', 'ocr_result', 'string', 'classification',
                  'confidence',
                  'application_id', 'application', 'task_uuid', 'classifytask', 'task')
        read_only_fields = ('application',)
        extra_kwargs = {
            'doc_type': {
                'required': False,
            },
            'sub_doc_type': {
                'required': False,
            },
        }


    def create(self, validated_data):
        document = super(ClassifySerializer, self).create(validated_data)
        application = Application.objects.filter(id=validated_data['application_id']).first()
        self.create_task('classifydocument', application, document)
        return document