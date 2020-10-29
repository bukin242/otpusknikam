# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Menu, MenuItem


class MenuInline(admin.TabularInline):

    model = MenuItem
    ordering = 'order', 'id'


class MenuAdmin(admin.ModelAdmin):

    list_display = 'name',
    ordering = 'id',
    inlines = (MenuInline, )


admin.site.register(Menu, MenuAdmin)
