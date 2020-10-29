# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django import template
from board.models import Board
from board.forms import FilterForm
from search.forms import SearchForm
import base64


register = template.Library()


@register.inclusion_tag('board/change_site.html')
def change_site(request):

    if request.site is not None:

        current_site = request.site

        return {
            'current_site': current_site,
            'sites': Site.objects.exclude(pk=current_site.pk)
        }

    else:
        return {
            'sites': Site.objects.all()
        }


@register.inclusion_tag('board/search_form.html', takes_context=True)
def search_form(context):

    request = context.get('request', {})

    if request:
        form = SearchForm(request.REQUEST)
    else:
        form = SearchForm

    return {'form': form}


@register.simple_tag
def encode_base64(value):

    try:
        count = (map(lambda x: len(x.strip()), value.split(','))[0] / 2)
    except Exception:
        count = 0

    value = ', '.join(map(lambda x: x.strip(), value.split(',')))

    return u"""
            $(function() {
                $('.phone_all').html(`%s <a href="#" class="phone_open" rel="%s"><small>Показать полностью</small></a>`);

                $('.phone_open').click(function(event) {
                  event.preventDefault();
                  hash = $(this).attr('rel');
                  $('.phone_all').text($.base64.atob(hash, true));
                  $('.protect').show();
                });
            });
            """ % (value[0:count], base64.b64encode(value.encode('utf8')))


@register.inclusion_tag('board/filter_form.html', takes_context=True)
def filter_form(context):

    request = context.get('request')

    if 'filter_submit' in request.GET:
        form = FilterForm(data=request.GET)
    else:
        form = FilterForm()

    if request.path == '/flat/' or request.path == '/':
        pass
    else:
        form.fields.pop('count')

    return {
        'form': form,
        'request': request
    }


@register.inclusion_tag('board/board_list_mini.html')
def board_list_mini(request):
    return {
        'object_list': Board.objects.filter(site=request.site)[:5]
    }
