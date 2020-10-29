# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import SearchListView


urlpatterns = patterns('',
    url(r'^$', SearchListView.as_view(), name='search_list'),
)
