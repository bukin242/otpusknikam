# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='board',
            name='number',
        ),
        migrations.AlterField(
            model_name='board',
            name='street',
            field=models.CharField(max_length=255, verbose_name='\u0430\u0434\u0440\u0435\u0441'),
        ),
    ]
