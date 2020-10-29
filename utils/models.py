# -*- coding: utf-8 -*-
import os
from django.db import models


def upload_dir_class_name(instance, filename):

    dirname = instance.__class__.__name__.lower()

    return os.path.join(dirname, filename)


class PublishedQuerySet(models.QuerySet):

    def published(self):
        return self.filter(published=True)

    def unpublished(self):
        return self.filter(published=False)


class PublishedManager(models.Manager):

    def get_queryset(self):
        return PublishedQuerySet(self.model)

    def published(self):
        return self.get_queryset().published()

    def unpublished(self):
        return self.get_queryset().unpublished()
