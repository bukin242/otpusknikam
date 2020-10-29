# -*- coding: utf-8 -*-
from elasticstack.views import SearchView
from haystack.query import SearchQuerySet
from forms import SearchForm


class SearchModelMixin(object):

    def get_context_data(self, **kwargs):

        context = super(SearchModelMixin, self).get_context_data(**kwargs)

        if self.model is not None:

            object_list = context.get('object_list', [])
            object_pks = map(lambda x: int(x.pk), object_list)
            object_list = self.model.objects.published().filter(pk__in=object_pks)

            context['object_list'] = object_list

        return context


class SearchListView(SearchView):

    object_list = None
    form_class = SearchForm
    queryset = SearchQuerySet()

    def get_context_data(self, **kwargs):

        context = super(SearchListView, self).get_context_data(**kwargs)

        context['count'] = self.queryset.count

        return context


class SearchModelListView(SearchModelMixin, SearchListView):

    model = None
