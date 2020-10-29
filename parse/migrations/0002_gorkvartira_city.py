# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20160908_0146'),
        ('parse', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gorkvartira',
            name='city',
            field=models.ForeignKey(default=1, verbose_name='\u0433\u043e\u0440\u043e\u0434', to='board.City'),
        ),
    ]
