# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site


class CheckSiteMiddleware(object):

    def process_request(self, request):

        try:
            get_current_site(request)
        except Site.DoesNotExist:
            try:
                request.META['HTTP_HOST'] = settings.DEFAULT_DOMAIN
            except IndexError:
                pass
