# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
        ('classifier', '0001_initial'),
        ('application', '0001_initial'),
        ('docset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('ready', models.BooleanField(default=True)),
                ('in_progress', models.BooleanField(default=False)),
                ('completed', models.BooleanField(default=False)),
                ('worker_uuid', models.CharField(default='', max_length=36)),
                ('result', models.TextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('application', models.ForeignKey(to='application.Application')),
                ('classifier', models.OneToOneField(null=True, to='classifier.Classifier')),
                ('classify', models.OneToOneField(null=True, related_name='classifytask', to='document.Document')),
                ('docset', models.OneToOneField(null=True, to='docset.DocSet')),
                ('document', models.OneToOneField(null=True, related_name='documenttask', to='document.Document')),
            ],
        ),
    ]
