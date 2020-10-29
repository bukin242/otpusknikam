# -*- coding: utf-8 -*-
from models import Page, MetaTags


def seo_page(request):

    try:

        obj_page = Page.objects.get(url=request.path)
        site_city = request.site.city

        try:
            obj = MetaTags.objects.get(url=request.path, city=site_city)
        except MetaTags.DoesNotExist:
            obj = obj_page

        for k, v in obj.__dict__.items():

            if isinstance(v, basestring):
                value = v
                if not value:
                    value = obj_page.__dict__.get(k, '')

                obj.__dict__[k] = value.format(city=site_city)

        return obj.__dict__

    except Page.DoesNotExist:
        return {}
