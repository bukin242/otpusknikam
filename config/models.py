# -*- coding: utf-8 -*-
from django.db import models


class Var(models.Model):

    name = models.SlugField(u'название настройки (ENG)', max_length=255)
    value = models.TextField(u'значение', blank=True)
    text_field = models.BooleanField(u'в поле "Значение" хранится HTML текст', db_index=True, default=False)
    description = models.CharField(u'описание настройки', max_length=255, blank=True, help_text=u'Необязательное поле для админки')
    published = models.BooleanField(u'включена', db_index=True, default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'настройку'
        verbose_name_plural = u'настройки'
        ordering = ['name']
