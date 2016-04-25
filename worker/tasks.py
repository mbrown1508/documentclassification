from __future__ import absolute_import
from celery import shared_task
from worker.worker import Worker


@shared_task
def start_worker():
    Worker()

