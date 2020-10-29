# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from redactor.widgets import RedactorEditor


class FlatPageOverridesAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.base_fields['sites'].initial = [settings.SITE_ID]
        self.base_fields['url'].help_text = 'Полный URL от корня сайта. Например /pages/'
        super(FlatPageOverridesAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FlatPage
        widgets = {
            'content': RedactorEditor()
        }
        exclude = []


class FlatPageOverridesAdmin(FlatPageAdmin):

    form = FlatPageOverridesAdminForm
    list_display = 'title', 'url'

    def __init__(self, *args, **kwargs):

        try:
            if 'fields' in self.fieldsets[0][1] and 'fields' in self.fieldsets[1][1]:
                self.fieldsets[0][1]['fields'] = filter(lambda x: x != 'sites', self.fieldsets[0][1]['fields'])
                self.fieldsets[1][1]['fields'] += ('sites', )
        except IndexError:
            pass

        super(FlatPageOverridesAdmin, self).__init__(*args, **kwargs)


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageOverridesAdmin)
