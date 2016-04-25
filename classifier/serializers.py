from rest_framework import serializers

from application.models import Application
from classifier.models import Classifier
from task.models import Task

class ClassifierSerializer(serializers.HyperlinkedModelSerializer):
    application_id = serializers.IntegerField()
    docset_id = serializers.IntegerField()
    task_uuid = serializers.ReadOnlyField(source='task.uuid')
    task = serializers.HyperlinkedRelatedField(read_only=True,  view_name='task-detail')

    class Meta:
        model = Classifier
        fields = ('url', 'id', 'name', 'random_forest_classifier', 'forest_tree_count',
                  'confidence', 'svc_classifier', 'doc_stats', 'bow',
                  'tfidf_vectoriser', 'bow_vectoriser', 'vec_analyzer', 'vec_min_df',
                  'vec_stop_words', 'vec_max_features', 'vec_ngram_range_min',
                  'vec_ngram_range_max', 'vec_strip_accents',
                  'application_id', 'application',
                  'docset_id', 'docset', 'task_uuid', 'task')
        read_only_fields = ('application', 'docset', )

    def create(self, validated_data):
        classifier = super(ClassifierSerializer, self).create(validated_data)
        application = Application.objects.filter(id=validated_data['application_id']).first()

        # Create a task to finish the work
        task=Task()
        task.type = 'createclassifier'
        task.application = application
        task.classifier = classifier
        task.save()

        return classifier

    def validate_application_id(self, value):
        if not Application.objects.filter(id=value).exists():
            raise serializers.ValidationError('{} is not a valid application id.'.format(value))
        return value