# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moon', '0003_auto_20160730_0142'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuimodel',
            name='lukou',
            field=models.CharField(default=b'no', max_length=100, verbose_name=b'send to lulou', blank=True),
        ),
    ]
