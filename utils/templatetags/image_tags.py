# -*- coding: utf-8 -*-
import os.path
from django import template
from decimal import Decimal
from django.conf import settings


FMT = 'JPEG'
EXT = 'jpg'
QUAL = 65
BLANK_IMAGE = os.path.join(settings.MEDIA_URL, 'base/blank.jpg')

register = template.Library()


def resized_path(path, size, method):
    "Returns the path for the resized image."

    dir, name = os.path.split(path)
    image_name, ext = os.path.splitext(name)

    return os.path.join(dir, '%s_%s_%s%s' % (image_name, method, size, ext))


def scale(imagefield, size, method='scale'):
    """
    Template filter used to scale an image
    that will fit inside the defined area.

    Returns the url of the resized image.

    {% load image_tags %}
    {{ profile.picture|scale:"48x48" }}
    """

    # imagefield can be a dict with "path" and "url" keys
    if imagefield.__class__.__name__ == 'dict':
        imagefield = type('imageobj', (object,), imagefield)

    image_path = resized_path(imagefield.path, size, method)

    if not os.path.exists(image_path):
        try:
            import Image
        except ImportError:
            try:
                from PIL import Image
            except ImportError:
                raise ImportError('Cannot import the Python Image Library.')

        try:
            image = Image.open(imagefield.path)
            FMT = image.format
        except:
            return BLANK_IMAGE

        try:
            tr = image.info.get('transparency', 0)

        except:
            pass

        # normalize image mode
        if image.mode not in ['RGB', 'RGBA', 'P']:
            image = image.convert('RGB')

        # parse size string 'WIDTHxHEIGHT'
        width, height = [int(i) for i in size.split('x')]

        # use PIL methods to edit images
        if method == 'scale':
            image.thumbnail((width, height), Image.ANTIALIAS)
            if FMT == 'GIF' and image.mode == 'P':
                image.save(image_path, FMT, quality=QUAL, transparency=tr)
            else:
                image.save(image_path, FMT, quality=QUAL)

        elif method == 'crop':
            try:
                import ImageOps
            except ImportError:
                from PIL import ImageOps

            if FMT == 'GIF' and image.mode == 'P':
                ImageOps.fit(
                    image, (width, height), Image.ANTIALIAS).save(image_path, FMT, quality=QUAL, transparency=tr)
            else:
                ImageOps.fit(
                    image, (width, height), Image.ANTIALIAS).save(image_path, FMT, quality=QUAL)

    return resized_path(imagefield.url, size, method)


def crop(imagefield, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|crop:"48x48" }}

    """
    return scale(imagefield, size, 'crop')


def auto_size(imagefield, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|auto_size:"48x48" }}

    """

    try:
        image_width = imagefield.width
        image_height = imagefield.height

        size_width, size_height = [int(i) for i in size.split('x')]

        if image_height < image_width:

            height = int((Decimal(size_width) / Decimal(image_width)) * int(image_height))
            size = '%sx%s' % (size_width, height)

        elif image_height > image_width:

            width = int((Decimal(size_height) / Decimal(image_height)) * int(image_width))
            size = '%sx%s' % (width, size_height)

    except TypeError:

        return BLANK_IMAGE

    return scale(imagefield, size, 'crop')


def from_width(imagefield, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|from_width:"48" }}

    """
    height = int((Decimal(size) / Decimal(imagefield.width)) * int(imagefield.height))
    size = '%sx%s' % (size, height)

    return scale(imagefield, size, 'crop')


def from_height(imagefield, size):
    """
    Template filter used to crop an image
    to make it fill the defined area.

    {% load image_tags %}
    {{ profile.picture|from_height:"48" }}

    """
    width = int((Decimal(size) / Decimal(imagefield.height)) * int(imagefield.width))
    size = '%sx%s' % (width, size)

    return scale(imagefield, size, 'crop')


register.filter('scale', scale)
register.filter('crop', crop)
register.filter('auto_size', auto_size)
register.filter('from_width', from_width)
register.filter('from_height', from_height)
