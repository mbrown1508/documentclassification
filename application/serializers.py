from rest_framework import serializers
from application.models import Application


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ('url', 'id', 'name')