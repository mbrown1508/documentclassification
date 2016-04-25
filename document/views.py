from rest_framework import viewsets

from document.models import Document
from document.serializers import DocumentSerializer, ClassifySerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        application_id = self.request.query_params.get('application', None)
        if application_id is not None:
            queryset = queryset.filter(application_id=application_id)
        return queryset

class ClassifyViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = ClassifySerializer

    def get_queryset(self):
        queryset = Document.objects.all()
        application_id = self.request.query_params.get('application', None)
        if application_id is not None:
            queryset = queryset.filter(application_id=application_id)
        return queryset