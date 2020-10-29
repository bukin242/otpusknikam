# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_city_head_verification'),
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaTags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(blank=True, max_length=255, verbose_name='\u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430', choices=[[b'/', b'/'], [b'/flat/', b'/flat/'], [b'/room/', b'/room/'], [b'/house/', b'/house/'], [b'/hostel/', b'/hostel/'], [b'/mini/', b'/mini/'], [b'/hotel/', b'/hotel/'], [b'/pension/', b'/pension/']])),
                ('title', models.CharField(max_length=255, blank=True)),
                ('keywords', models.CharField(max_length=255, blank=True)),
                ('description', models.TextField(blank=True)),
                ('seo_text', redactor.fields.RedactorField(verbose_name='SEO \u0442\u0435\u043a\u0441\u0442', blank=True)),
                ('city', models.ForeignKey(verbose_name='\u0433\u043e\u0440\u043e\u0434', blank=True, to='board.City', null=True)),
            ],
            options={
                'verbose_name': '\u043c\u0435\u0442\u0430-\u0442\u0435\u0433',
                'verbose_name_plural': '\u043c\u0435\u0442\u0430-\u0442\u0435\u0433\u0438',
            },
        ),
        migrations.RemoveField(
            model_name='page',
            name='seo_text',
        ),
    ]
