# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files.storage import default_storage
import os


class Image(ImageFile):

    def __init__(self, path, file=None, *args, **kwargs):

        file = default_storage.open(path)
        self.path = file.name
        self.url = os.path.join(settings.MEDIA_URL, path)

        super(Image, self).__init__(file, *args, **kwargs)
