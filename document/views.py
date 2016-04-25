from rest_framework import viewsets

from document.models import Document
from document.serializers import DocumentSerializer, ClassifySerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class ClassifyViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = ClassifySerializer