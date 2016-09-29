# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=400, verbose_name=b'email', blank=True)),
                ('send', models.CharField(max_length=100, verbose_name=b'is send', blank=True)),
                ('title', models.CharField(max_length=500, verbose_name=b'title', blank=True)),
                ('check', models.CharField(max_length=100, verbose_name=b'check count', blank=True)),
            ],
        ),
    ]
