# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView
from views import BoardWizard, image_upload, image_delete
from forms import BoardForm, FlatForm, PriceForm, ImageForm


urlpatterns = [
    url(r'^image_upload/$', image_upload, name='image_upload'),
    url(r'^image_delete/$', image_delete, name='image_delete'),
    url(r'^create/$', TemplateView.as_view(template_name='board/board_create.html'), name='board_create_select'),
    url(r'^create/(?P<type_realty>[-\w]+)/$', BoardWizard.as_view([BoardForm, FlatForm, PriceForm, ImageForm]), name='board_create'),
]
