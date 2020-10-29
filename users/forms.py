# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from models import SiteUser, Profile
from utils.forms import FormMixin


def validate_password_length(value):

    min_length = 5

    if len(value) < min_length:
        raise ValidationError(u'Пароль должен быть минимум {length} символов.'.format(length=min_length))


class LoginForm(FormMixin, AuthenticationForm):
    pass


class RegistrationForm(FormMixin, forms.ModelForm):

    email = forms.EmailField(
        label=u'E-mail адрес',
        widget=forms.TextInput
    )
    password = forms.CharField(
        label=u'Пароль',
        widget=forms.PasswordInput,
        validators=[validate_password_length]
    )
    password2 = forms.CharField(
        label=u'Повтор пароля',
        widget=forms.PasswordInput,
        validators=[validate_password_length]
    )

    class Meta:

        model = SiteUser
        fields = ['email', 'password', 'password2']

    def clean(self):

        super(RegistrationForm, self).clean()

        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Пароли не совпадают. Пожалуйста повторите попытку.")

        return self.cleaned_data

    def save(self, commit=True):

        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        return user


class ProfileRegistrationForm(FormMixin, forms.ModelForm):

    class Meta:

        model = Profile
        fields = ['name', 'email', 'password', 'subscribe']

    def __init__(self, *args, **kwargs):

        super(ProfileRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['password'].validators.append(validate_password_length)
        self.fields['password'].widget = forms.PasswordInput()

    def save(self, *args, **kwargs):

        self.instance.set_password(self.instance.password)

        super(ProfileRegistrationForm, self).save(*args, **kwargs)
