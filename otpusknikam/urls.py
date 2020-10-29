# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from board.views import BoardListView, BoardDetailView, SearchListView, get_phone
from articles.views import ArticleListView, ArticleDetailView
from django.contrib.sitemaps import views as sitemaps_views
from sitemaps import sitemaps


if settings.DEBUG:

    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    ]

else:

    urlpatterns = []

urlpatterns += [
    url(r'^sitemap.xml$',
        sitemaps_views.index, {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^(?P<section>.+)\.xml$',
        sitemaps_views.sitemap, {'sitemaps': sitemaps}, name='sitemaps'),
]

urlpatterns += [
    url(r'^$', BoardListView.as_view(), name='board_list'),
    url(r'^search/$', SearchListView.as_view(), name='search_list'),
    url(r'^user/(?P<user_pk>\d+)/$', BoardListView.as_view(), name='board_list_user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^accounts/', include('users.urls')),
    url(r'^board/', include('board.urls')),
    url(r'^realty/$', ArticleListView.as_view(), name='article_list'),
    url(r'^realty/(?P<slug>[-_\w]+)/(?P<pk>\d+)\.html', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^(?P<type_realty>[-\w]+)/$', BoardListView.as_view(), name='board_list_type_realty'),
    url(r'^(?P<type_realty>[-\w]+)/(?P<pk>\d+)/$', BoardDetailView.as_view(), name='board_detail'),
    url(r'^(?P<type_realty>[-\w]+)/(?P<pk>\d+)/phone\.js$', get_phone, name='board_phone'),
    url(r'^robots\.txt', 'robots.views.robots'),
    url(r'^', include('django.contrib.flatpages.urls')),
]
