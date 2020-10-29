# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0002_auto_20170512_0046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='metatags',
            options={'ordering': ['city__city_name', 'url'], 'verbose_name': '\u043c\u0435\u0442\u0430-\u0442\u0435\u0433', 'verbose_name_plural': '\u043c\u0435\u0442\u0430-\u0442\u0435\u0433\u0438'},
        ),
        migrations.AddField(
            model_name='metatags',
            name='header',
            field=models.CharField(max_length=255, verbose_name='h1', blank=True),
        ),
    ]
