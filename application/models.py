from django.db import models

class Application(models.Model):
    app_label = 'application'

    name = models.CharField(max_length=100)