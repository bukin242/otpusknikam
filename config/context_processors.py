# -*- coding: utf-8 -*-
from django.conf import settings


def var(request):
    return {'config': settings.CONFIG}
