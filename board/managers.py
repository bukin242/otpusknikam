# -*- coding: utf-8 -*-
from django.db import models
from utils.models import PublishedManager


class ImageManager(models.Manager):

    def get_queryset(self):
        return super(ImageManager, self).get_queryset().select_related('board')


class BoardManager(PublishedManager):

    def get_queryset(self):
        return super(BoardManager, self).get_queryset().select_related('city', 'price', 'flat', 'room', 'house', 'hostel', 'mini', 'hotel', 'pension')
