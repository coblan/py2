# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moon', '0002_auto_20160730_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'name', blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='tuimodel',
            name='tag',
        ),
        migrations.AddField(
            model_name='tuimodel',
            name='tag',
            field=models.ManyToManyField(to='moon.Tag', null=True, blank=True),
        ),
    ]
