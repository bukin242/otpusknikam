# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from board.models import City, Board
from parse.models import GorKvartira, text
from parse.utils import parse_url
import random
import logging
import time


logging.basicConfig(level=logging.CRITICAL)

CITY = City.objects.get(domain='otpusknikam.ru')

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        boards = Board.objects.filter(city=CITY).exclude(name__icontains=u'в санкт-петербурге').exclude(name__icontains=u'в петербурге').exclude(name__icontains=u'в спб').exclude(name__icontains=u'в питере').filter(name__icontains=u'в ')

        for x in boards:
            try:
                doc = parse_url(x.gorkvartira.url)
                title = text(doc.xpath('//title')).lower()
                if not bool(u'в санкт-петербурге' in title):
                    print x.gorkvartira.url
                    x.delete()
                    time.sleep(0.1)
            except:
                print x.pk
