# -*- coding: utf-8 -*-
from django.contrib import admin
from parse.models import GorKvartira


class GorKvartiraAdmin(admin.ModelAdmin):
    list_display = '__unicode__',

admin.site.register(GorKvartira, GorKvartiraAdmin)
