# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from board.models import City
from parse.models import GorKvartira, text
from parse.utils import parse_url
import random
import logging
import time


logging.basicConfig(level=logging.CRITICAL)

HOST = 'http://gorkvartira.ru%s'

URLS = {
    'adler.otpusknikam.ru': 'http://gorkvartira.ru/city/adler',
    'alushta.otpusknikam.ru': 'http://gorkvartira.ru/city/alushta',
    'anapa.otpusknikam.ru': 'http://gorkvartira.ru/city/anapa',
    'glz.otpusknikam.ru': 'http://gorkvartira.ru/city/gelendzhik',
    'ept.otpusknikam.ru': 'http://gorkvartira.ru/city/evpatoria',
    'estk.otpusknikam.ru': 'http://gorkvartira.ru/city/essentuki',
    'kerch.otpusknikam.ru': 'http://gorkvartira.ru/city/kerch',
    'ksv.otpusknikam.ru': 'http://gorkvartira.ru/city/kislovodsk',
    'moscow.otpusknikam.ru': 'http://gorkvartira.ru/city/moscow',
    'otpusknikam.ru': 'http://gorkvartira.ru/city/saint-petersburg',
    'stp.otpusknikam.ru': 'http://gorkvartira.ru/city/sevastopol',
    'sochi.otpusknikam.ru': 'http://gorkvartira.ru/city/sochi',
    'sudak.otpusknikam.ru': 'http://gorkvartira.ru/city/sudak',
    'tuapse.otpusknikam.ru': 'http://gorkvartira.ru/city/tuapse',
    'yalta.otpusknikam.ru': 'http://gorkvartira.ru/city/yalta',
}

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        for k, v in URLS.items():
            city = City.objects.get(domain=k)
            doc_page = parse_url(v)
            urls = map(lambda x: x.get('href'), doc_page.cssselect('.data .grid .inter h2 a'))
            random.shuffle(urls)

            print k

            for y in urls:
                url = HOST % y

                if not GorKvartira.objects.filter(url=url).exists():
                    GorKvartira.objects.create(**{
                        'city': city,
                        'url': url,
                    })

                    print text(parse_url(url).xpath('//title'))

                    time.sleep(0.5)
