# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GorKvartira',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(unique=True, max_length=512, verbose_name='URL')),
                ('error', models.TextField(verbose_name='\u043e\u0448\u0438\u0431\u043a\u0438', blank=True)),
                ('board', models.OneToOneField(related_name='gorkvartira', null=True, blank=True, to='board.Board')),
            ],
        ),
    ]
