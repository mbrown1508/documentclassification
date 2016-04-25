from rest_framework import viewsets

from docset.models import DocSet
from docset.serializers import DocSetSerializer


class DocSetViewSet(viewsets.ModelViewSet):
    queryset = DocSet.objects.all()
    serializer_class = DocSetSerializer