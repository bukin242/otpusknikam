# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0005_auto_20170528_1048'),
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-pk'], 'verbose_name': '\u0441\u0442\u0430\u0442\u044c\u044e', 'verbose_name_plural': '\u0441\u0442\u0430\u0442\u044c\u0438'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='order',
        ),
        migrations.AddField(
            model_name='article',
            name='city',
            field=models.ForeignKey(verbose_name='\u0433\u043e\u0440\u043e\u0434', blank=True, to='board.City', null=True),
        ),
    ]
