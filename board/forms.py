# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import BaseModelFormSet, modelformset_factory
from django.contrib.auth import authenticate
from models import Board, Flat, Room, House, Hostel, Mini, Hotel, Pension, Price, Discount, PriceMonth, OwnPrice, Image, ROOM_COUNT
from utils.forms import FormMixin, CustomErrorMixin
from users.forms import SiteUser, validate_password_length
from time import time
import md5


def get_data_step(data, step, field_name):
    return data.get('{}-{}'.format(step, field_name), u'')


class BoardForm(FormMixin, forms.ModelForm):

    name_register = forms.CharField(
        label=u'Имя на сайте',
        widget=forms.TextInput
    )
    email_register = forms.EmailField(
        label=u'E-mail адрес',
        widget=forms.TextInput
    )
    subscribe_register = forms.BooleanField(
        label=u'подписка на предложения',
        required=False
    )
    password_register = forms.CharField(
        label=u'Пароль',
        widget=forms.PasswordInput,
        validators=[validate_password_length]
    )
    email_login = forms.EmailField(
        label=u'E-mail адрес',
        widget=forms.TextInput
    )
    password_login = forms.CharField(
        label=u'Пароль',
        widget=forms.PasswordInput,
        validators=[validate_password_length]
    )

    class Meta:
        model = Board
        fields = '__all__'

    def is_valid(self):

        if self.request.user.is_authenticated():

            self.errors.pop('email_login', None)
            self.errors.pop('password_login', None)
            self.errors.pop('name_register', None)
            self.errors.pop('email_register', None)
            self.errors.pop('password_register', None)

        else:

            email_register = get_data_step(self.data, self.step, 'email_register')
            email_login = get_data_step(self.data, self.step, 'email_login')

            if email_register and not email_login:
                self.errors.pop('email_login', None)
                self.errors.pop('password_login', None)
            elif email_login and not email_register:
                self.errors.pop('name_register', None)
                self.errors.pop('email_register', None)
                self.errors.pop('password_register', None)

        return super(BoardForm, self).is_valid()

    def clean(self):

        email_register = self.cleaned_data.get('email_register', '')
        email_login = self.cleaned_data.get('email_login', '')

        if email_register:
            if SiteUser.objects.filter(email=email_register).exists():
                self.add_error('email_register', u'Пользователь с таким E-mail уже существует.')

        elif email_login:
            password_login = self.cleaned_data.get('password_login', '')

            if not authenticate(email=email_login, password=password_login):
                self.add_error('email_login', u'Пользователя с таким E-mail и паролем не существует.')

        return self.cleaned_data


class FlatForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Flat
        exclude = 'board',


class RoomForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Room
        exclude = 'board',


class HouseForm(FormMixin, forms.ModelForm):

    class Meta:
        model = House
        exclude = 'board',


class HostelForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Hostel
        exclude = 'board',


class MiniForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Mini
        exclude = 'board',


class HotelForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Hotel
        exclude = 'board',


class PensionForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Pension
        exclude = 'board',


class PriceForm(FormMixin, forms.ModelForm):

    class Meta:
        model = Price
        exclude = 'board',


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = 'board',

    def __init__(self, *args, **kwargs):

        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['hash_image'].widget = forms.HiddenInput()

        if hasattr(self, 'request'):

            get_hash = getattr(self.request, 'hash', '')

            if not get_hash:
                self.request.hash = md5.new(str(time())).hexdigest()

            self.fields['hash_image'].initial = self.request.hash

    def clean(self):

        if self.cleaned_data.get('image') is None:
            self.cleaned_data = {}

        return self.cleaned_data

    def save(self, commit=True):

        if hasattr(self, 'cleaned_data') and self.cleaned_data:
            return super(ImageForm, self).save(commit)


class FormSetMixin(CustomErrorMixin, BaseModelFormSet):

    def __init__(self, *args, **kwargs):

        kwargs.setdefault('prefix', self.model.__name__.lower())

        super(FormSetMixin, self).__init__(*args, **kwargs)

    def get_queryset(self):

        return self.model.objects.none()


DiscountFormSet = modelformset_factory(Discount, formset=FormSetMixin, exclude=('board', ), extra=5, max_num=5)
PriceMonthFormSet = modelformset_factory(PriceMonth, formset=FormSetMixin, exclude=('board', ), extra=12, max_num=12)
OwnPriceFormSet = modelformset_factory(OwnPrice, formset=FormSetMixin, exclude=('board', ), extra=3, max_num=3)
ImageFormSet = modelformset_factory(Image, formset=FormSetMixin, exclude=('board', ), extra=20, max_num=20, form=ImageForm)


TYPE_REALTY_FORM = {
    'flat': FlatForm,
    'room': RoomForm,
    'house': HouseForm,
    'hostel': HostelForm,
    'mini': MiniForm,
    'hotel': HotelForm,
    'pension': PensionForm,
}

PRICE = [
    ('', 'По цене'),
    ('desc', 'От меньшей'),
    ('asc', 'От большей'),
]

class FilterForm(forms.Form):

    price = forms.ChoiceField(label=u'', choices=PRICE, required=False)
    count = forms.ChoiceField(label=u'', choices=[('', 'Кол-во комнат')] + ROOM_COUNT, required=False)
