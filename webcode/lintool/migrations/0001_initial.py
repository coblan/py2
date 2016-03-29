# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WorksModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('func', models.CharField(max_length=300, verbose_name=b'\xe5\x87\xbd\xe6\x95\xb0\xe5\x90\x8d', blank=True)),
                ('kw', models.TextField(verbose_name=b'\xe5\x85\xb3\xe9\x94\xae\xe5\xad\x97\xe5\x8f\x82\xe6\x95\xb0', blank=True)),
                ('rt', models.TextField(verbose_name=b'\xe8\xbf\x94\xe5\x9b\x9e\xe7\xbb\x93\xe6\x9e\x9c', blank=True)),
                ('sud_time', models.DateTimeField(auto_now=True, verbose_name=b'\xe5\xba\x94\xe8\xaf\xa5\xe5\xa4\x84\xe7\x90\x86\xe6\x97\xb6\xe5\x88\xbb', null=True)),
                ('fetched', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe8\xa2\xab\xe8\xae\xa4\xe9\xa2\x86')),
                ('done', models.BooleanField(default=False, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\xb7\xb2\xe5\xa4\x84\xe7\x90\x86')),
                ('category', models.CharField(max_length=100, verbose_name=b'\xe7\xb1\xbb\xe5\x9e\x8b', blank=True)),
            ],
        ),
    ]
