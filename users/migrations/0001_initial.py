# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(unique=True, max_length=255, verbose_name='e-mail \u0430\u0434\u0440\u0435\u0441')),
                ('create_date', models.DateTimeField(db_index=True, auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('balance', models.IntegerField(default=200, verbose_name='\u0431\u0430\u043b\u0430\u043d\u0441')),
                ('name', models.CharField(max_length=255, verbose_name='\u0438\u043c\u044f \u043d\u0430 \u0441\u0430\u0439\u0442\u0435')),
                ('subscribe', models.BooleanField(default=False, db_index=True, verbose_name='\u043f\u043e\u0434\u043f\u0438\u0441\u043a\u0430 \u043d\u0430 \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u043f\u0440\u043e\u0444\u0438\u043b\u044c',
                'verbose_name_plural': '\u043f\u0440\u043e\u0444\u0438\u043b\u0438',
            },
            bases=('users.siteuser',),
        ),
    ]
