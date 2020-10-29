# -*- coding: utf-8 -*-
from haystack import indexes
from models import Board


class BoardIndex(indexes.ModelSearchIndex, indexes.Indexable):

    site_id = indexes.IntegerField(model_attr='site_id', null=True)
    price = indexes.IntegerField(model_attr='price__price', null=True)

    class Meta:

        model = Board

    def index_queryset(self, using=None):

        return Board.objects.published()
