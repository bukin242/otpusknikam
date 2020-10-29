# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u043f\u043e\u0437\u0438\u0446\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u043c\u0435\u043d\u044e',
                'verbose_name_plural': '\u043c\u0435\u043d\u044e',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('url', models.CharField(max_length=255, verbose_name='URL', blank=True)),
                ('order', models.IntegerField(default=0, verbose_name='\u043f\u043e\u0437\u0438\u0446\u0438\u044f', blank=True)),
                ('parent', models.ForeignKey(verbose_name='\u0440\u043e\u0434\u0438\u0442\u0435\u043b\u044c', blank=True, to='menu.Menu', null=True)),
            ],
            options={
                'ordering': ['order', 'pk'],
                'verbose_name': '\u043f\u0443\u043d\u043a\u0442',
                'verbose_name_plural': '\u043f\u0443\u043d\u043a\u0442\u044b',
            },
        ),
    ]
