# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20170528_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='site',
            field=models.ForeignKey(related_name='article_articles', to='sites.Site', null=True),
        ),
    ]
