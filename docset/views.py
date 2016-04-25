from rest_framework import viewsets

from docset.models import DocSet
from docset.serializers import DocSetSerializer


class DocSetViewSet(viewsets.ModelViewSet):
    serializer_class = DocSetSerializer
    queryset = DocSet.objects.all()

    def get_queryset(self):
        queryset = DocSet.objects.all()
        application_id = self.request.query_params.get('application', None)
        if application_id is not None:
            queryset = queryset.filter(application_id=application_id)
        return queryset