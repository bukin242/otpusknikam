# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.conf import settings


class PublishedMixin(View):

    def get_queryset(self):
        return super(PublishedMixin, self).get_queryset().published()


class PaginateByMixin(View):

    paginate_by = getattr(settings, 'PAGINATE_BY', 0)

    def get_context_data(self, **kwargs):
        context = super(PaginateByMixin, self).get_context_data(**kwargs)

        queries_page = self.request.GET.copy()
        queries_page.pop('page', '')

        if queries_page:
            queries_page = ''.join(map(lambda x: '&%s=%s' % (x[0], x[1]), queries_page.items()))
        else:
            queries_page = ''

        context['queries'] = queries_page

        return context

class LoginRequiredMixin(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)
