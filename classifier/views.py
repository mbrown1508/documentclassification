from rest_framework import viewsets

from classifier.models import Classifier
from classifier.serializers import ClassifierSerializer


class ClassifierViewSet(viewsets.ModelViewSet):
    queryset = Classifier.objects.all()
    serializer_class = ClassifierSerializer