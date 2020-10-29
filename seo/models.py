# -*- coding: utf-8 -*-
from django.db import models
from redactor.fields import RedactorField
from board.models import City


META_PAGES = [
    ['/']*2,
    ['/flat/']*2,
    ['/room/']*2,
    ['/house/']*2,
    ['/hostel/']*2,
    ['/mini/']*2,
    ['/hotel/']*2,
    ['/pension/']*2,
]


class MetaTags(models.Model):

    url = models.CharField(u'страница', choices=META_PAGES, max_length=255, blank=True)
    city = models.ForeignKey(City, verbose_name=u'город', null=True, blank=True)
    header = models.CharField(u'h1', max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    keywords = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    seo_text = RedactorField(u'SEO текст', blank=True)

    def __unicode__(self):
        return '%s [ %s ]' % (self.city.city_name, self.url)

    class Meta:

        verbose_name = u'мета-тег'
        verbose_name_plural = u'мета-теги'
        ordering = ['city__city_name', 'url']


class Page(models.Model):

    url = models.CharField(u'URL', max_length=255, unique=True, help_text=u'Полный URL от корня сайта. Например /pages/')
    header = models.CharField(u'h1', max_length=255, blank=True)
    title = models.CharField(u'title страницы', max_length=255, blank=True)
    keywords = models.CharField(u'keywords', max_length=255, blank=True)
    description = models.CharField(u'description', max_length=255, blank=True)

    def __unicode__(self):
        return self.url

    class Meta:
        verbose_name = u'настройка'
        verbose_name_plural = u'SEO настройки'
        ordering = ['url']
