# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from board.models import Image


@receiver(pre_save, sender=Image)
def save_image(sender, instance, **kwargs):

    if instance.pk and instance.main and instance.board is not None:
        instance.board.image_main = instance.image
        instance.board.save(update_fields=['image_main'])
