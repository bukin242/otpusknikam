# -*- coding: utf-8 -*-
from django.conf.urls import url
from honeypot.decorators import check_honeypot
from views import register_view, login_view, logout_view, AccountView, AccountHideBoardView
from forms import ProfileRegistrationForm

urlpatterns = [
    url(r'^$', AccountView.as_view(), name='account_list'),
    url(r'^board/(?P<pk>\d+)/hide/$', AccountHideBoardView.as_view(), name='account_hide'),
    url(r'^register/$', check_honeypot(register_view), kwargs={'register_form': ProfileRegistrationForm}, name='users_register'),
    url(r'^login/$', check_honeypot(login_view), name='users_login'),
    url(r'^logout/$', logout_view, name='users_logout'),
]
