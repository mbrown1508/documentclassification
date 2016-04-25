# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=256)),
                ('ocr_result', models.TextField(null=True)),
                ('string', models.TextField(null=True)),
                ('doc_type', models.CharField(null=True, max_length=100)),
                ('sub_doc_type', models.CharField(null=True, max_length=100)),
                ('classification', models.CharField(null=True, max_length=100)),
                ('confidence', models.IntegerField(null=True)),
                ('hash', models.CharField(null=True, max_length=36)),
                ('raw_string', models.TextField(null=True)),
                ('clean_string', models.TextField(null=True)),
                ('page_count', models.IntegerField(null=True)),
                ('word_count', models.IntegerField(null=True)),
                ('unique_word_count', models.IntegerField(null=True)),
                ('char_count', models.IntegerField(null=True)),
                ('upper_case_percent', models.FloatField(null=True)),
                ('lower_case_percent', models.FloatField(null=True)),
                ('number_percent', models.FloatField(null=True)),
                ('symbol_percent', models.FloatField(null=True)),
                ('space_percent', models.FloatField(null=True)),
                ('application', models.ForeignKey(to='application.Application')),
            ],
        ),
    ]
