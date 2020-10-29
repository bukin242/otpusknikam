# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('slug', models.SlugField(max_length=255, verbose_name='\u0442\u0435\u043a\u0441\u0442 \u0432 \u0442\u0440\u0430\u043d\u0441\u043b\u0438\u0442\u0435 \u0434\u043b\u044f URL', blank=True)),
                ('text', models.TextField(verbose_name=b'\xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82')),
                ('image', models.ImageField(upload_to=b'article', verbose_name='\u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('order', models.IntegerField(default=0, verbose_name='\u043f\u043e\u0437\u0438\u0446\u0438\u044f')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': '\u0441\u0442\u0430\u0442\u044c\u044e',
                'verbose_name_plural': '\u0441\u0442\u0430\u0442\u044c\u0438',
            },
        ),
    ]
