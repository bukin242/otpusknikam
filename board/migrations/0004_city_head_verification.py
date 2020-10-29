# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_auto_20160917_2318'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='head_verification',
            field=models.TextField(verbose_name='head meta \u0442\u0435\u0433\u0438', blank=True),
        ),
    ]
