# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_city_head_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='type_realty',
            field=models.CharField(default=b'flat', max_length=255, verbose_name='\u0442\u0438\u043f \u043d\u0435\u0434\u0432\u0438\u0436\u0438\u043c\u043e\u0441\u0442\u0438 \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0432\u044b \u0445\u043e\u0442\u0438\u0442\u0435 \u0441\u0434\u0430\u0442\u044c', db_index=True, choices=[(b'flat', '\u041a\u0432\u0430\u0440\u0442\u0438\u0440\u0443'), (b'room', '\u041a\u043e\u043c\u043d\u0430\u0442\u0443'), (b'house', '\u0414\u043e\u043c'), (b'hostel', '\u0425\u043e\u0441\u0442\u0435\u043b'), (b'mini', '\u041c\u0438\u043d\u0438-\u043e\u0442\u0435\u043b\u044c'), (b'hotel', '\u0413\u043e\u0441\u0442\u0438\u043d\u0438\u0446\u0443'), (b'pension', '\u0421\u0430\u043d\u0430\u0442\u043e\u0440\u0438\u0439')]),
        ),
    ]
