# -*- coding: utf-8 -*-
from django.db.models.fields.files import FileField
from django.db.models.signals import post_delete


def auto_delete_files(sender, instance, **kwargs):

    for x in instance._meta.fields:

        if isinstance(x, FileField):
            object_file = x.value_from_object(instance)

            if bool(object_file) and x.storage.exists(object_file):
                x.storage.delete(object_file)


post_delete.connect(auto_delete_files)
