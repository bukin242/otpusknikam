# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from board.models import City
from parse.models import GorKvartira, text
from parse.utils import parse_url
import random
import logging
import time


logging.basicConfig(level=logging.CRITICAL)

CITY = City.objects.get(domain='moscow.otpusknikam.ru')
HOST = 'http://gorkvartira.ru%s'
URL = 'http://gorkvartira.ru/city/moscow?page=%s'

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        doc = parse_url(URL)
        page = int(text(doc.cssselect('.pagination a:last-child')))

        for x in reversed(xrange(1, page + 1)):

            doc_page = parse_url(URL % x)
            urls = map(lambda x: x.get('href'), doc_page.cssselect('.data .grid .inter h2 a'))
            random.shuffle(urls)

            for y in urls:

                if not GorKvartira.objects.filter(url=HOST % y).exists():
                    GorKvartira.objects.create(**{
                        'city': CITY,
                        'url': HOST % y,
                    })

                    time.sleep(0.1)

            print x
