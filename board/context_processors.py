# -*- coding: utf-8 -*-
from models import TYPE_REALTY, TYPE_REALTY_LIST


def var(request):

    result = {'type_realty_all': TYPE_REALTY}

    if hasattr(request, 'resolver_match'):

        type_realty = request.resolver_match.kwargs.get('type_realty')
        if type_realty in TYPE_REALTY_LIST:
            result.update({'type_realty': type_realty})

    return result
