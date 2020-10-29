# -*- coding: utf-8 -*-
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from models import Var


@receiver(post_save, sender=Var)
def config_reload(sender, **kwargs):

    path = 'reload'
    if os.path.isfile(path):
        os.utime(path, None)
