# -*- coding: utf-8 -*-
from haystack.forms import SearchForm as HaystackSearchForm


class SearchForm(HaystackSearchForm):

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)

        q = self.fields['q']
        q.widget.attrs.update({'placeholder': u'Я ищу...'})
