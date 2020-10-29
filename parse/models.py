# -*- coding: utf-8 -*-
from django.db import models
from board.models import Board, City, Flat, Price, Image
from django.contrib.sites.models import Site
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from users.models import SiteUser
from utils import parse_url
from PIL import Image as PILImage, ImageDraw, ImageFont, ImageFilter
import requests
import traceback
import random
import re
import os


USER = SiteUser.objects.get(email=u'bukin242@yandex.ru')
HOST = 'http://gorkvartira.ru'
VALIDATE = URLValidator()
FONT = os.path.join(settings.MEDIA_ROOT, 'base/FreeMono.ttf')

def text(value):

    if value:
        return value[0].text_content().strip()
    else:
        return ''


def comma_text(value):

    value = value.split(',')
    value = map(lambda x: x if x and x[0] == ' ' else ' %s' % x, value)

    return ','.join(value)


def random_text(value):

    value = value.split('.')
    value = filter(lambda x: x.strip(' ') != '', value)
    value = map(lambda x: ' %s' % x, value)
    random.shuffle(value)

    return '.'.join(value)


class GorKvartira(models.Model):
    city = models.ForeignKey(City, verbose_name=u'город', default=1)
    url = models.URLField(u'URL', max_length=512, unique=True)
    board = models.OneToOneField(Board, related_name='%(class)s', null=True, blank=True)
    error = models.TextField(u'ошибки', blank=True)

    def save(self, *args, **kwargs):
        if self.board:
            return None

        try:
            doc = parse_url(self.url)

            root = doc.cssselect('.content .rwide')[0]
            standart = root.cssselect('.standard[width="100%"]')[0]

            h1 = text(doc.xpath('//h1'))
            title = text(doc.xpath('//title'))
            address = doc.xpath('//div[@class="spacer"]/div[@style="float:left"]/text()')
            content = root.text_content().lower()
            count = int(h1[0])

            if content.find(u'студия') > 0 or content.find(u'студию') > 0 or content.find(u'студии') > 0:
                h1 = h1.replace(u'квартира ', u'').replace(u'%s-комнатная ' % count, u'Студия ')
                title = title.replace(u'квартира ', u'').replace(u'%s-комнатная ' % count, u'Студия ')
                names = [h1, title, title.replace(u'посуточно ', u'')]

                count = 0

            else:

                names = [h1, h1.replace(u'комнатная ', u'к. '), title, title.replace(u'посуточно ', u''), title.replace(u'комнатная ', u'к. '), title.replace(u'посуточно ', u'').replace(u'комнатная ', u'к. ')]

            name = random.choice(names)

            if address:
                address = comma_text(address[0].replace('> ', '').strip())
            else:
                return None

            if self.city.metro:
                bpad = text(root.cssselect('.bpad'))
                metro = re.findall(u'(\d+) мин.', bpad, re.UNICODE | re.IGNORECASE)
                if metro:
                    metro = int(metro[0])
                else:
                    metro = None
            else:
                metro = None

            try:
                phone = text(root.xpath(u"//*[contains(text(),'Тел.:')]/ancestor::tr[1]")[0].cssselect('td:last-child'))
            except Exception:
                phone = ''

            try:
                contact_name = text(root.xpath("//td/span/a[contains(@href,'/info/')]")).split(',')[0]
            except Exception:
                contact_name = ''

            try:
                floor = text(standart.xpath(u"//*[contains(text(),'Этаж')]/ancestor::tr[1]")[0].cssselect('td:last-child'))
                floor = re.findall(u'(\d+)', floor, re.UNICODE | re.IGNORECASE)
                floor_number = floor[0]
                if len(floor) >= 2:
                    floors = floor[1]
                else:
                    floors = None
            except Exception:
                floor_number = 0
                floors = None

            try:
                total_space = text(standart.xpath(u"//*[contains(text(),'Площадь')]/ancestor::tr[1]")[0].cssselect('td:last-child'))
                total_space = re.findall(u'(\d+)', total_space, re.UNICODE | re.IGNORECASE)[0]
            except Exception:
                total_space = 0

            try:
                sleep = text(standart.xpath(u"//*[contains(text(),'Спальные места')]/ancestor::tr[1]")[0].cssselect('td:last-child'))
                sleep = re.findall(u'(\d+)', sleep, re.UNICODE | re.IGNORECASE)
                sleep = sum(map(int, sleep))
            except Exception:
                sleep = 1

            try:
                price = int(text(standart.cssselect('.spacer .bigger')))
            except Exception:
                price = None

            try:
                description = text(standart.xpath(u"//*[contains(text(),'Описание')]/ancestor::td[1]//p"))
                description = random_text(comma_text(description))
            except Exception:
                description = ''

            try:
                bron_condition = text(standart.xpath(u"//*[contains(text(),'Условия бронирования')]/ancestor::td[1]//p"))
                placement_condition = text(standart.xpath(u"//*[contains(text(),'Условия размещения')]/ancestor::td[1]//p"))

                other_condition = ('%s \n%s' % (random_text(comma_text(bron_condition)), placement_condition)).strip()
            except Exception:
                other_condition = ''

            try:
                available = text(standart.xpath(u"//*[contains(text(),'В распоряжении гостей')]/ancestor::td[1]/dt")).lower()
            except Exception:
                available = ''

            self.board = Board.objects.create(**{
                'city': self.city,
                'site': Site.objects.get(domain=self.city.domain),
                'user': USER,
                'name': name,
                'metro': metro,
                'street': address,
                'phone': phone,
                'contact_name': contact_name,
                'text': description,
            })

            try:
                images = doc.cssselect('.fancybox')
                images = map(lambda x: x.get('href'), images)
                images = filter(None, images)
                images = map(lambda x: '%s%s' % (HOST, x), images)

                for i, x in enumerate(images):
                    try:
                        VALIDATE(x)
                        result = requests.get(x)
                        if result.ok:
                            basename = os.path.basename(x)

                            image = NamedTemporaryFile(delete=True, suffix=os.path.splitext(basename)[1])
                            image.write(result.content)

                            im = PILImage.open(image)
                            width, height = im.size
                            im = im.crop((0, 0, width, height-25))
                            im = im.filter(ImageFilter.DETAIL)

                            draw = ImageDraw.Draw(im)
                            font = ImageFont.truetype(FONT, 20)
                            draw.text((random.choice([10, width-180]), random.choice([10, height-50])), "otpusknikam.ru", font=font, fill=(255, 255, 255, 128))

                            im.save(image.name, optimize=True)

                            image_file = File(image)
                            board_image = Image(board=self.board)
                            board_image.image.save(basename, image_file)

                            if i == 0:
                                self.board.image_main = board_image.image
                                self.board.save(force_update=True)
                                board_image.main = True

                    except ValidationError:
                        pass

            except Exception:
                pass

            #Flat['repair', 'total_space', 'living_space', 'heater', 'attractions', 'other_comfort', 'mirror', '_state', 'bars', 'other_condition', 'floors', 'sleep', 'microwave', 'housing_estate', 'table', 'conditioner', 'cafe', 'parking', 'id', 'market', 'balcony', 'board_id', 'dishes', 'tv', 'linens', 'museum', 'kettle', 'elevator', 'cinema', 'protected', 'lions', 'forest', 'animal', 'internet', 'party', 'washer', 'shopping_center', 'type_bed', 'fast_food', 'waterpark', 'coffee', 'cupboard', 'around', 'shower_cabine', 'park', 'bike', 'phone', 'floor_number', 'fan', 'boat_trips', 'child', 'frig', 'pizzeria', 'kitchen', 'count', 'smoke', 'salon', 'theater', 'cooker', 'spa', 'stores', 'nightclub', 'type_house', 'iron', 'nightstand', 'document', 'restaurants']

            Flat.objects.create(**{
                'board': self.board,
                'total_space': total_space,
                'floor_number': floor_number,
                'floors': floors,
                'sleep': sleep,
                'balcony': bool(u'балкон' in content),
                'elevator': bool(u'лифт' in content),
                'count': count,
                'other_condition': other_condition,

                'tv': bool(u'телевизор' in available),
                'phone': False,
                'conditioner': bool(u'кондиционер' in available),
                'fan': False,
                'heater': False,
                'linens': False,
                'washer': bool(u'стиральная машина' in available),
                'shower_cabine': False,
                'table': False,
                'cupboard': False,
                'nightstand': False,
                'mirror': False,
                'iron': False,
                'dishes': False,
                'frig': bool(u'холодильник' in available),
                'microwave': bool(u'микроволновая печь' in available),
                'coffee': False,
                'kettle': False,
                'parking': bool(u'парковочное место' in available),
                'protected': False,
                'internet': False,
                'stores': False,
                'market': False,
                'shopping_center': False,
                'bars': False,
                'cafe': False,
                'restaurants': False,
                'pizzeria': False,
                'fast_food': False,
                'salon': False,
                'nightclub': False,
                'spa': False,
                'boat_trips': False,
                'bike': False,
                'attractions': False,
                'waterpark': False,
                'museum': False,
                'theater': False,
                'cinema': False,
                'park': False,
                'forest': False,
                'document': False,
                'around': False,
                'child': False,
                'animal': False,
                'smoke': False,
                'party': False,
            })

            Price.objects.create(**{
                'board': self.board,
                'price': price,
                'clearing': False,
                'agreement': False,
                'documents': bool(u'документы для отчетности: да' in content),
            })

            self.error = ''

        except Exception:
            self.error = traceback.format_exc()

        super(GorKvartira, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.url
