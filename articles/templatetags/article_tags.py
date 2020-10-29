# -*- coding: utf-8 -*-
from django import template
from articles.models import Article


register = template.Library()


@register.inclusion_tag('articles/article_list_mini.html')
def article_list_mini(request):
    return {
        'object_list': Article.objects.filter(site=request.site)[:9]
    }
