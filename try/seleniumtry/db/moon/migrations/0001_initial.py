# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TuiModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=700, verbose_name=b'url', blank=True)),
                ('img', models.CharField(max_length=700, verbose_name=b'img', blank=True)),
                ('title', models.CharField(max_length=700, verbose_name=b'title', blank=True)),
                ('price', models.CharField(max_length=100, verbose_name=b'price', blank=True)),
            ],
        ),
    ]
