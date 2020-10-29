# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect
from formtools.wizard.views import SessionWizardView
from users.forms import ProfileRegistrationForm, LoginForm
from users.models import SiteUser, Profile
from forms import TYPE_REALTY_FORM, BoardForm, PriceForm, ImageForm, DiscountFormSet, PriceMonthFormSet, OwnPriceFormSet, ImageFormSet, FilterForm, get_data_step
from models import TYPE_REALTY, TYPE_REALTY_LIST, Image, Board
from utils.views import PaginateByMixin, PublishedMixin
from search.views import SearchModelListView
from templatetags.board_tags import encode_base64
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter
import json
import random
import os
import re


FIND_ID = re.compile(ur'[-\w]+\[(\d+)\]', re.U | re.I)
FONT = os.path.join(settings.MEDIA_ROOT, 'base/UbuntuMono-B.ttf')


class BoardWizard(SessionWizardView):

    template_name = 'board/board_form.html'
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'temp'))
    price_form_sets = [DiscountFormSet, PriceMonthFormSet, OwnPriceFormSet]

    @staticmethod
    def get_form_set(formset_class, data={}, files={}, prefix=''):

        form_data = {}

        if not prefix:
            prefix = formset_class.model.__name__.lower()

        if prefix:
            prefix = '%s-' % prefix

        for k, v in data.items():

            if k.startswith(prefix):
                form_data.update({k: v})

        return formset_class(data=form_data, files=files)

    def dispatch(self, request, *args, **kwargs):

        self.type_realty = self.kwargs.get('type_realty', '')
        self.from_step = self.request.REQUEST.get('from_step', '')

        try:
            str(self.request.site.city)
        except self.request.site.DoesNotExist:
            self.request.site = None

        if self.type_realty not in TYPE_REALTY_LIST:
            self.type_realty = None

        return super(BoardWizard, self).dispatch(request, *args, **kwargs)

    def get_form_initial(self, step):

        initial = super(BoardWizard, self).get_form_initial(step)

        if self.type_realty is not None:
            initial.update(self.kwargs)

        if self.request.site is not None:
            initial.update({'city': self.request.site.pk})

        return initial

    def get_form_prefix(self, step=None, form=None):

        form.step = step
        form.request = self.request

        if step == u'0':

            form.base_fields['type_realty'].widget = forms.HiddenInput()

            if self.request.site is not None:
                form.base_fields['city'].widget = forms.HiddenInput()

        elif step == u'1':

            form = TYPE_REALTY_FORM.get(self.type_realty)
            self.form_list.update({u'1': form})

        return super(BoardWizard, self).get_form_prefix(step, form)

    def process_step(self, form):

        form_data = super(BoardWizard, self).process_step(form)
        step_index = str(self.get_step_index())

        type_realty = get_data_step(form_data, step_index, 'type_realty')

        if not type_realty or type_realty in TYPE_REALTY_FORM:
            type_realty = self.type_realty

        form = TYPE_REALTY_FORM.get(type_realty)
        self.form_list.update({u'1': form})

        return form_data

    def post(self, *args, **kwargs):

        form = self.get_form(data=self.request.POST, files=self.request.FILES)

        if isinstance(form, PriceForm):

            for x in self.price_form_sets:
                form_set = self.get_form_set(x, data=form.data, files=self.request.FILES)

                if form_set.data and not form_set.is_valid():
                    return self.render(form)

        elif isinstance(form, ImageForm):
            nojs = form.data.get('image-TOTAL_FORMS', 0)

            if nojs and form.data and form.data.get('hash_image', ''):
                form_set = self.get_form_set(ImageFormSet, data=form.data, files=self.request.FILES)

                if form_set.data and not form_set.is_valid():
                    return self.render(form)

        return super(BoardWizard, self).post(*args, **kwargs)

    def get_context_data(self, form, **kwargs):

        context = super(BoardWizard, self).get_context_data(form, **kwargs)

        context['form_register'] = ProfileRegistrationForm(self.request.POST or {})
        context['form_login'] = LoginForm(self.request.POST or {})

        if isinstance(form, PriceForm):

            if self.request.method == 'POST' and self.from_step == u'2':

                context['form_discount'] = DiscountFormSet(self.request.POST)
                context['form_pricemonth'] = PriceMonthFormSet(self.request.POST)
                context['form_ownprice'] = OwnPriceFormSet(self.request.POST, files=self.request.FILES)
            else:
                context['form_discount'] = DiscountFormSet()
                context['form_pricemonth'] = PriceMonthFormSet()
                context['form_ownprice'] = OwnPriceFormSet()

        elif isinstance(form, ImageForm):

            if self.request.method == 'POST' and self.from_step == u'3':

                context['form_image'] = ImageFormSet(self.request.POST, files=self.request.FILES)
            else:
                context['form_image'] = ImageFormSet(initial=[{'order': x} for x in xrange(ImageFormSet.extra)])

        context['type_realty'] = self.type_realty
        context['type_realty_name'] = dict(TYPE_REALTY).get(self.type_realty, '')

        if self.request.site is not None:
            context['city'] = self.request.site.city

        return context

    def done(self, form_list, **kwargs):

        board = None
        user = None

        if self.request.user.is_authenticated() and not self.request.user.is_anonymous():

            user = self.request.user

        for x in form_list:

            if isinstance(x, ImageForm):

                main = x.data.get('main', '')
                nojs = x.data.get('image-TOTAL_FORMS', 0)

                if nojs:
                    if main:
                        x.data.update({main: u'on'})

                    image_form = self.get_form_set(ImageFormSet, data=x.data, files=x.files)

                    if image_form.data and image_form.is_valid():
                        image_form.save()

                else:
                    if main:
                        Image.objects.filter(pk=main).update(main=True)

                    data_name = {}
                    data_order = {}

                    for k, v in x.data.items():
                        if v:
                            ids = map(int, FIND_ID.findall(k))
                            if ids:
                                if k.startswith('name'):
                                    data_name.update({ids[0]: v})
                                elif k.startswith('order'):
                                    data_order.update({ids[0]: v})

                    for k, v in data_name.items():
                        Image.objects.filter(pk=k).update(name=v)

                    for k, v in data_order.items():
                        Image.objects.filter(pk=k).update(order=v)

                hash_image = x.data.get('hash_image', '')

                if hash_image and board is not None:
                    Image.objects.filter(hash_image=hash_image).update(board=board)

                    if main:
                        image_qs = board.image.filter(main=True, image__isnull=False)
                        if image_qs.exists():
                            board.image_main = image_qs[0].image
                            board.save(update_fields=['image_main'])

                if not nojs:
                    Image.objects.filter(board__isnull=True).delete()

            else:

                obj = x.save()

                if isinstance(x, BoardForm):

                    if user is None:

                        email_register = x.cleaned_data.get('email_register', '')
                        email_login = x.cleaned_data.get('email_login', '')

                        if email_register:
                            name_register = x.cleaned_data.get('name_register', '')
                            password_register = x.cleaned_data.get('password_register', '')
                            subscribe_register = x.cleaned_data.get('subscribe_register', '')
                            profile = Profile.objects.create_user(name=name_register, email=email_register, password=password_register, subscribe=subscribe_register)
                            user = authenticate(email=profile.email, password=password_register)

                        elif email_login:

                            password_login = x.cleaned_data.get('password_login', '')
                            user = authenticate(email=email_login, password=password_login)

                        if user is not None:
                            login(self.request, user)

                    obj.user = user
                    obj.site = self.request.site
                    obj.published = True
                    obj.save(update_fields=['user', 'site', 'published'])

                    board = obj

                else:

                    if board is not None:

                        obj.board = board
                        obj.save(update_fields=['board'])

                        if isinstance(x, PriceForm):

                            for f in self.price_form_sets:
                                form_set = self.get_form_set(f, data=x.data, files=x.files)

                                if form_set.data and form_set.is_valid():
                                    form_objs = form_set.save()

                                    for o in form_objs:
                                        o.board = board
                                        o.save(update_fields=['board'])

        messages.success(self.request, u'Ваше объявление добавлено.')

        return redirect('account_list')


@csrf_exempt
def image_upload(request):

    response = {'status': 'success'}
    status = 404

    if request.method == 'POST':

        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save()

            if obj is not None:
                im = PILImage.open(obj.image.path)
                width, height = im.size
                limit_width, limit_height = 1920, 1080

                if width > limit_width or height > limit_height:
                    if width > limit_width:
                        height = int((float(limit_width) / float(width)) * float(height))
                        width = limit_width
                    elif height > limit_height:
                        width = int((float(limit_height) / float(height)) * float(width))
                        height = limit_height

                    im = im.resize((width, height))

                im = im.crop((0, 0, width, height-25))
                im = im.filter(ImageFilter.DETAIL)

                draw = ImageDraw.Draw(im)
                font = ImageFont.truetype(FONT, 32)
                draw.text((random.choice([10, width-250]), random.choice([10, height-80])), "otpusknikam.ru", font=font, fill=(255, 255, 255, 128))

                im.save(obj.image.path, optimize=True)

                response.update({'pk': obj.pk})
                status = 200
            else:
                response.update({'error': u'Ошибка при сохранении.'})

        else:
            if form.errors:
                response.update({'error': form.errors.as_text()})

    return HttpResponse(json.dumps(response), content_type="application/json", status=status)


@csrf_exempt
def image_delete(request):

    response = {'status': 'success'}

    if request.method == 'POST':

        hash_image = request.POST.get('hash_image', '')
        pk = int(request.POST.get('pk', 0))

        if hash_image and pk:
            Image.objects.filter(hash_image=hash_image, pk=pk).delete()

    return HttpResponse(json.dumps(response), content_type="application/json")


def get_phone(request, type_realty, pk):
    obj = get_object_or_404(Board, pk=pk)
    return HttpResponse(encode_base64(obj.phone or ''), content_type='application/javascript')


class FilterBaseView(View):

    def get_filter(self, qs, search=False):

        if 'filter_submit' in self.request.GET:
            form = FilterForm()
            form.data = self.request.GET
            form.is_bound = True
            form.full_clean()

            price = form.cleaned_data.get('price')
            count = form.cleaned_data.get('count', '')

            if price:

                if search:
                    price_name = 'price'
                else:
                    price_name = 'price__price'

                if price == 'desc':
                    qs = qs.order_by(price_name)
                else:
                    qs = qs.order_by('-%s' % price_name)

            if count != '':
                try:
                    qs = qs.filter(flat__isnull=False).filter(flat__count=count)
                except Exception:
                    pass

        return qs

    def get_queryset(self):

        qs = super(FilterBaseView, self).get_queryset()
        qs = self.get_filter(qs)

        return qs


class BoardBaseView(PublishedMixin):

    def get_queryset(self):

        return super(BoardBaseView, self).get_queryset().filter(site=self.request.site)


class BoardListView(FilterBaseView, BoardBaseView, PaginateByMixin, ListView):

    model = Board

    def get_queryset(self):

        qs = super(BoardListView, self).get_queryset()

        self.type_realty = self.kwargs.get('type_realty')
        self.user_pk = self.kwargs.get('user_pk')
        self.user = None

        if self.type_realty:
            if self.type_realty in TYPE_REALTY_LIST:
                qs = qs.filter(type_realty=self.type_realty)
            else:
                raise Http404
        elif self.user_pk:
            self.user = get_object_or_404(SiteUser, pk=self.user_pk)
            qs = qs.filter(user=self.user)

        return qs

    def get_context_data(self, **kwargs):

        context = super(BoardListView, self).get_context_data(**kwargs)
        context['from_user'] = self.user

        return context


class BoardDetailView(BoardBaseView, DetailView):

    model = Board


class SearchListView(FilterBaseView, PaginateByMixin, SearchModelListView):

    model = Board
    template_name = 'board/board_list.html'

    def get_query_set(self):

        qs = super(SearchListView, self).get_query_set()

        if self.request.site is not None:
            qs = qs.filter(site_id=self.request.site.pk)

        return self.get_filter(qs, search=True)
