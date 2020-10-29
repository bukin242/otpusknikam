# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from models import Var


class VarAdmin(admin.ModelAdmin):

    list_display = 'name', 'description', 'published',
    list_editable = 'published',


admin.site.register(Var, VarAdmin)
