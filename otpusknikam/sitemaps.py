# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap, GenericSitemap
from board.models import Board
from menu.models import MenuItem


class PagesSitemap(Sitemap):

    urls = [
        '/'
    ]

    urls += MenuItem.objects.all().values_list('url', flat=True)

    def items(self):
        return range(len(self.urls))

    def location(self, obj):
        return self.urls[obj]


class BoardSitemap(GenericSitemap):

    site = None

    def get_urls(self, *args, **kwargs):

        self.site = kwargs.get('site')

        return super(BoardSitemap, self).get_urls(*args, **kwargs)

    def items(self):

        qs = self.queryset

        if self.site is not None:
            qs = qs.filter(site=self.site)

        return qs


sitemaps = {

    'pages': PagesSitemap(),

    'board': BoardSitemap({
        'queryset': Board.objects.published()
    }),

}
