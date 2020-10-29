# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage
from django.db.models.signals import pre_save
from django.dispatch import receiver
from menu.models import Menu, MenuItem


@receiver(pre_save, sender=FlatPage)
def save_page(sender, instance, *args, **kwargs):

    if not instance.pk:
        for x in Menu.objects.filter(name='bottom'):
            if not x.menuitem_set.filter(url=instance.url).exists():
                x.menuitem_set.create(name=instance.title, url=instance.url)
    else:
        page = sender.objects.get(pk=instance.pk)
        MenuItem.objects.filter(url=page.url).update(url=instance.url)
