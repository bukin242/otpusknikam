# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ValidationError


def max_file_size_validator(field):

    megabyte_limit = getattr(settings, 'MAX_FILE_SIZE_UPLOAD', 0)

    if megabyte_limit:

        if bool(field.file) and int(field.file.size) > megabyte_limit * 1024 * 1024:
            raise ValidationError(u'Максимально допустимый размер файла: {filesize}МБ.'.format(filesize=str(megabyte_limit)))
