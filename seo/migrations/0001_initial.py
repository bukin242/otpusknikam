# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(help_text='\u041f\u043e\u043b\u043d\u044b\u0439 URL \u043e\u0442 \u043a\u043e\u0440\u043d\u044f \u0441\u0430\u0439\u0442\u0430. \u041d\u0430\u043f\u0440\u0438\u043c\u0435\u0440 /pages/', unique=True, max_length=255, verbose_name='URL')),
                ('title', models.CharField(max_length=255, verbose_name='title \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b', blank=True)),
                ('header', models.CharField(max_length=255, verbose_name='h1', blank=True)),
                ('keywords', models.CharField(max_length=255, verbose_name='keywords', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name='description', blank=True)),
                ('seo_text', redactor.fields.RedactorField(verbose_name='SEO \u0442\u0435\u043a\u0441\u0442', blank=True)),
            ],
            options={
                'ordering': ['url'],
                'verbose_name': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430',
                'verbose_name_plural': 'SEO \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438',
            },
        ),
    ]
