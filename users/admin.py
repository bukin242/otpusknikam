# -*- coding: utf-8 -*-
from django.contrib import admin
from models import SiteUser, Profile


class SiteUserAdmin(admin.ModelAdmin):
    list_display = 'email', 'create_date',

    def save_model(self, request, obj, form, change):

        if change:
            old = self.model.objects.get(pk=obj.pk)

            if old.password != obj.password:
                obj.set_password(obj.password)

        else:
            obj.set_password(obj.password)

        super(SiteUserAdmin, self).save_model(request, obj, form, change)


class ProfileAdmin(admin.ModelAdmin):
    list_display = '__unicode__', 'user'
    exclude = 'password', 'user',


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(Profile, ProfileAdmin)
