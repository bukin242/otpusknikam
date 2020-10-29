# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('articles', '0002_auto_20170528_1048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='city',
        ),
        migrations.AddField(
            model_name='article',
            name='site',
            field=models.ForeignKey(related_name='article_articles', blank=True, to='sites.Site', null=True),
        ),
    ]
