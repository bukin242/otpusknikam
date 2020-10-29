# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DeleteView, View
from board.models import Board
from utils.views import LoginRequiredMixin, PaginateByMixin
from users.forms import RegistrationForm
from forms import LoginForm


REGISTER_URL = reverse_lazy('users_register')
LOGIN_URL = reverse_lazy('users_login')
LOGOUT_URL = reverse_lazy('users_logout')


def login_view(request, register_form=RegistrationForm, login_form=LoginForm):

    next = request.REQUEST.get('next')
    if next and next != REGISTER_URL and next != LOGIN_URL and next != LOGOUT_URL:
        success_url = next
    else:
        success_url = '/'

    if request.method == 'POST':
        form = login_form(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(success_url)
    else:
        if request.user.is_authenticated():
            logout(request)

        form = login_form()
    return render_to_response('users/login.html', {
        'form': form,
        'register_form': register_form,
    }, context_instance=RequestContext(request))


def register_view(request, register_form=RegistrationForm):

    next = request.REQUEST.get('next')
    if next and next != REGISTER_URL and next != LOGIN_URL and next != LOGOUT_URL:
        success_url = next
    else:
        success_url = '/'

    if request.method == 'POST':
        form = register_form(data=request.POST)
        if form.is_valid():

            form.save()
            messages.info(request, u'Спасибо за регистрацию. Выполнен автоматический вход в аккаунт.')

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user_auth = authenticate(username=email, password=password)
            login(request, user_auth)

            return redirect(success_url)
    else:
        if request.user.is_authenticated():
            return redirect(success_url)

        form = register_form()
    return render_to_response('users/register.html', {
        'form': form,
    }, context_instance=RequestContext(request))


def logout_view(request):

    logout(request)
    return render_to_response('users/logout.html', context_instance=RequestContext(request))


class FromUserView(View):

    def get_queryset(self):

        return super(FromUserView, self).get_queryset().filter(user=self.request.user)


class AccountView(PaginateByMixin, LoginRequiredMixin, FromUserView, ListView):

    paginate_by = 100
    model = Board
    template_name = 'users/account_list.html'


class AccountHideBoardView(LoginRequiredMixin, FromUserView, DeleteView):

    model = Board
    template_name = 'users/account_hide_form.html'

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()

        if self.object.published:
            self.object.published = False
            messages.success(self.request, u'Объявление скрыто и не показывается на сайте.')

        else:
            self.object.published = True
            messages.success(self.request, u'Объявление вновь показывается на сайте.')

        self.object.save(update_fields=['published'])

        return redirect('account_list')
