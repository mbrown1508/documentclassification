# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocSet',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('train_percentage', models.IntegerField()),
                ('test_percentage', models.IntegerField()),
                ('application', models.ForeignKey(to='application.Application')),
                ('test_documents', models.ManyToManyField(related_name='test_documents', to='document.Document')),
                ('train_documents', models.ManyToManyField(related_name='train_documents', to='document.Document')),
            ],
        ),
    ]
