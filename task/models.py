from django.db import models
from uuid import uuid1

from classifier.models import Classifier
from docset.models import DocSet
from document.models import Document
from application.models import Application


class Task(models.Model):
    app_label = 'task'

    type = models.CharField(max_length=100)

    ready = models.BooleanField(default=True)
    in_progress = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    worker_uuid = models.CharField(max_length=36, default='')
    result = models.TextField(null=True)

    created = models.DateTimeField(auto_now_add=True)

    application = models.ForeignKey('application.Application')
    classifier = models.OneToOneField('classifier.Classifier', null=True)
    document = models.OneToOneField('document.Document', null=True, related_name='documenttask')
    docset = models.OneToOneField('docset.DocSet', null=True)
    classify = models.OneToOneField('document.Document', null=True, related_name='classifytask')