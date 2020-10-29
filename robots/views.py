# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import Context, Template
from django.http import Http404, HttpResponse


def robots(request):

    robots_template = settings.CONFIG.get('robots')

    if not robots_template:

        raise Http404

    else:

        template = Template(robots_template)
        context = Context({
            'scheme': request.scheme,
            'domain': request.get_host
        })
        text = template.render(context)

        return HttpResponse(text, content_type='text/plain')
