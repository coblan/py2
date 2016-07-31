# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuimodel',
            name='tag',
            field=models.CharField(max_length=700, verbose_name=b'tag', blank=True),
        ),
        migrations.AddField(
            model_name='tuimodel',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name=b'update time', null=True),
        ),
    ]
