from django.db import models

from document.models import Document

class DocSet(models.Model):
    app_label = 'docset'

    name = models.CharField(max_length=100)
    train_percentage = models.IntegerField()
    test_percentage = models.IntegerField()

    application = models.ForeignKey('application.Application')

    test_documents = models.ManyToManyField(Document, related_name='test_documents')
    train_documents = models.ManyToManyField(Document, related_name='train_documents')