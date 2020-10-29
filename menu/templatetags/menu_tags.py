# -*- coding: utf-8 -*-
from django.template import Library
from menu.models import MenuItem
from django.conf import settings


register = Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def menu(context, menu_name=''):

    request = context.get('request')
    object_list = MenuItem.objects.filter(parent__name=menu_name)
    menu_list = list(object_list)

    for x in menu_list:
        url = x.url

        if request.path == url:
            x.active = True

        else:
            x.active = False

    return {
        'object_list': object_list,
        'menu_name': menu_name
    }


@register.simple_tag(takes_context=True)
def edit(context):

    link = ''

    try:
        request = context.get('request')
        user = request.user
        obj = context.get('object')

        if obj and user and user.is_superuser:
            url = "/admin/%s/" % "/".join([obj._meta.app_label, obj._meta.module_name, str(obj.pk)])
            link = ' <a href="%s" class="edit_link" target="_blank" style="padding:0px; margin:0px; text-decoration:none; border:none;" title="Редактировать"><img src="%simages/edit.png" alt="Редактировать"></a>' % (url, settings.MEDIA_URL)

    except Exception:
        pass

    return link
