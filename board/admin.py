# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.sites.models import Site
from models import City, Board, Flat, Room, House, Hostel, Mini, Hotel, Pension, Discount, Price, PriceMonth, OwnPrice, Image


class ImageAdmin(admin.ModelAdmin):

    list_display = '__unicode__', 'main', 'order', 'board',
    ordering = '-id',

class BoardAdmin(admin.ModelAdmin):

    search_fields = 'id',


admin.site.unregister(Site)
admin.site.register(City)
admin.site.register(Board, BoardAdmin)
admin.site.register(Flat)
admin.site.register(Room)
admin.site.register(House)
admin.site.register(Hostel)
admin.site.register(Mini)
admin.site.register(Hotel)
admin.site.register(Pension)
admin.site.register(Discount)
admin.site.register(Price)
admin.site.register(PriceMonth)
admin.site.register(OwnPrice)
admin.site.register(Image, ImageAdmin)
