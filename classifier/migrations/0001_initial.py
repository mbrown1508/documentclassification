# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docset', '0001_initial'),
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('random_forest_classifier', models.BooleanField(default=True)),
                ('forest_tree_count', models.IntegerField(default=2000)),
                ('confidence', models.IntegerField(default=0)),
                ('svc_classifier', models.BooleanField(default=False)),
                ('doc_stats', models.BooleanField(default=True)),
                ('bow', models.BooleanField(default=True)),
                ('tfidf_vectoriser', models.BooleanField(default=False)),
                ('bow_vectoriser', models.BooleanField(default=True)),
                ('vec_analyzer', models.CharField(default='word', max_length=20)),
                ('vec_min_df', models.FloatField(default=0.001)),
                ('vec_stop_words', models.CharField(default='english', max_length=20)),
                ('vec_max_features', models.IntegerField(default=10000)),
                ('vec_ngram_range_min', models.IntegerField(default=1)),
                ('vec_ngram_range_max', models.IntegerField(default=3)),
                ('vec_strip_accents', models.CharField(default='ascii', max_length=20)),
                ('application', models.ForeignKey(to='application.Application')),
                ('docset', models.ForeignKey(to='docset.DocSet')),
            ],
        ),
    ]
