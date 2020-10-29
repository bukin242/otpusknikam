# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Var',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.SlugField(max_length=255, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 (ENG)')),
                ('value', models.TextField(verbose_name='\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', blank=True)),
                ('text_field', models.BooleanField(default=False, db_index=True, verbose_name='\u0432 \u043f\u043e\u043b\u0435 "\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435" \u0445\u0440\u0430\u043d\u0438\u0442\u0441\u044f HTML \u0442\u0435\u043a\u0441\u0442')),
                ('description', models.CharField(help_text='\u041d\u0435\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0435 \u043f\u043e\u043b\u0435 \u0434\u043b\u044f \u0430\u0434\u043c\u0438\u043d\u043a\u0438', max_length=255, verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438', blank=True)),
                ('published', models.BooleanField(default=True, db_index=True, verbose_name='\u0432\u043a\u043b\u044e\u0447\u0435\u043d\u0430')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0443',
                'verbose_name_plural': '\u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438',
            },
        ),
    ]
