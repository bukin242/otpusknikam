# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.sites.models import Site


class Article(models.Model):

    site = models.ForeignKey(Site, related_name='%(class)s_%(app_label)s', null=True)
    name = models.CharField(u'название', max_length=255)
    slug = models.SlugField(u'текст в транслите для URL', max_length=255, blank=True)
    text = models.TextField('текст')
    image = models.ImageField(u'изображение', upload_to='article', null=True, blank=True)

    class Meta:
        verbose_name = u'статью'
        verbose_name_plural = u'статьи'
        ordering = ['-pk']

    @models.permalink
    def get_absolute_url(self):
        return 'article_detail', [self.slug, self.pk]

    def __unicode__(self):
        return self.name
