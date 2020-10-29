# -*- coding: utf-8 -*-
from django.db import models


class Menu(models.Model):

    name = models.CharField(u'позиция', max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'меню'
        verbose_name_plural = 'меню'


class MenuItem(models.Model):

    parent = models.ForeignKey(Menu, verbose_name=u'родитель', null=True, blank=True)
    name = models.CharField(u'название', max_length=255)
    url = models.CharField(u'URL', max_length=255, blank=True)
    order = models.IntegerField(u'позиция', blank=True, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['order', 'pk']
        verbose_name = 'пункт'
        verbose_name_plural = 'пункты'

    def get_absolute_url(self):
        return self.url
