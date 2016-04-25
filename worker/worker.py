from time import sleep
from uuid import uuid1
from task.models import Task

from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from worker.helperclasses.dictionary import Dictionary

from document.models import Document
from random import randint
from worker.classifier import Classifier
from worker.cache.cache import Cache

import json

class Worker:
    def __init__(self):
        self.uuid = str(uuid1())
        self.application = None
        self.classifier = None
        self.dictionary = Dictionary()
        self.main()

    def main(self):
        while True:
            self.get_work()
            self.complete_work()

            sleep(1)



    def complete_work(self):
        for task in self.tasks:
            if task.type == 'createdocument':
                result = self.add_document(task)
            elif task.type == 'createdocset':
                result = self.create_document_set(task)
            elif task.type == 'createclassifier':
                result = self.create_classifier(task)
            elif task.type == 'classifydocument':
                result = self.classify_document(task)
            else:
                raise Exception('The task type is invalid.')

            self.mark_task_complete(task, result)



    def get_work(self):
        # If the application is set get any work for them
        count = 0
        if self.application is not None:
            nested_q = Task.objects.filter(application=self.application,
                                           ready=True,
                                           in_progress=False)[:10]
            count = Task.objects.filter(pk__in=nested_q).update(ready=False,
                                                                in_progress=True,
                                                                worker_uuid=self.uuid)

        # If we didn't find anything do work anyone can do
        if count == 0:
            nested_q = Task.objects \
                           .filter(ready=True, in_progress=False) \
                           .exclude(Q(type='createclassifier') | Q(type='classifydocument'))[:10]

            count = Task.objects.filter(pk__in=nested_q).update(ready=False,
                                                                in_progress=True,
                                                                worker_uuid=self.uuid)

        # do work that we have to change classifiers for
        if count == 0:
            try:
                application_obj = Task.objects.filter(ready=True, in_progress=False).earliest('created')
            except Task.DoesNotExist:
                application_obj = None

            if application_obj is not None:
                application = application_obj.application

                nested_q = Task.objects.filter(application=application,
                                               ready=True,
                                               in_progress=False,
                                               created__lt=timezone.now() - timedelta(seconds=10))[:10]
                Task.objects.filter(pk__in=nested_q).update(ready=False,
                                                            in_progress=True,
                                                            worker_uuid=self.uuid)

        # get the tasks that the worker got
        self.tasks = Task.objects.filter(worker_uuid=self.uuid,
                                    in_progress=True)


    def add_document(self, task):
        task.document.create_values(dictionary=self.dictionary)
        task.document.save()
        return 'Document created'

    def create_document_set(self, task):
        # Get a list of all the documents
        doc_types = set(Document.objects.values_list('doc_type', flat=True)\
                                    .filter(application=task.application))

        document_dictionary = {}
        for doc_type in doc_types:
            document_dictionary[doc_type] = Document.objects.filter(doc_type=doc_type,
                                                                    application=task.application)

        # For each document type create a list of random numbesrs from 0-100
        # If the number is over the train percentage it is in the test set ect
        # Check that there is at least 1 document in each set or redo the random
        # skip doc_types that have only 1 or less document
        for doc_type in doc_types:
            if len(document_dictionary[doc_type]) < 2:
                continue

            # Generate random array
            generating_array = True
            doc_distribution = []
            while generating_array:
                doc_distribution = [randint(0, 100) for _ in range(len(document_dictionary[doc_type]))]
                if max(doc_distribution) > task.docset.train_percentage:
                    generating_array = False

            # Allocate documents
            for document_index in range(len(doc_distribution)):
                if doc_distribution[document_index] > task.docset.train_percentage:
                    task.docset.test_documents.add(document_dictionary[doc_type][document_index])
                else:
                    task.docset.train_documents.add(document_dictionary[doc_type][document_index])

        task.docset.save()
        return 'DocSet Created'

    ## Requires Model

    def classify_document(self, task):
        if not self.check_application(task):
            return 'No valid classifier'

        task.classify.create_values(dictionary=self.dictionary)
        task.classify.save()

        self.classifier.predict(task.classify)

        result = self.classifier.get_forests_single_doc()

        if result['doc_type'] == None:
            result['doc_type'] = 'Unknown'

        task.classify.classification = result['doc_type']
        task.classify.save()

        return 'Document Classified'

    def create_classifier(self, task):
        # Create Classifier
        self.application = task.application
        self.classifier = Classifier(task.classifier)
        self.classifier.train_classifier()

        # Cache model
        Cache.store(task.classifier, self.classifier)

        return 'Classifier Created'

    def mark_task_complete(self, task, result):
        task.completed = True
        task.in_progress = False
        task.ready = False
        task.result = result
        task.save()

    def check_application(self, task):
        if self.application is None or self.application.id != task.application.id:
            classifiers = list(task.application.classifier_set.all())
            if len(classifiers) > 0:
                self.application = task.application
                self.classifier = Cache.load(classifiers[-1])
            else:
                return False
        return True