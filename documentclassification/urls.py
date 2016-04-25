from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from application.views import ApplicationViewSet
from document.views import DocumentViewSet, ClassifyViewSet
from docset.views import DocSetViewSet
from task.views import TaskViewSet
from classifier.views import ClassifierViewSet

router = DefaultRouter()
router.register(r'application', ApplicationViewSet)
router.register(r'document', DocumentViewSet, 'document')
router.register(r'docset', DocSetViewSet)
router.register(r'task', TaskViewSet)
router.register(r'classifier', ClassifierViewSet)
router.register(r'classify', ClassifyViewSet, 'classify')

# fix here http://stackoverflow.com/questions/24351287/django-rest-framework-two-different-modelserializers-for-the-same-model

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^document/$', DocumentViewSet.as_view({'get': 'list'}), name='document-list'),
    url(r'^document/(?P<pk>[0-9]+)/$', DocumentViewSet.as_view({'get': 'retrieve'}), name='document-detail'),
]