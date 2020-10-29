# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.safestring import mark_safe
from utils.models import upload_dir_class_name
from utils.validators import max_file_size_validator
from managers import ImageManager, BoardManager


TYPE_REALTY = [
    ('flat', u'Квартиру'),
    ('room', u'Комнату'),
    ('house', u'Дом'),
    ('hostel', u'Хостел'),
    ('mini', u'Мини-отель'),
    ('hotel', u'Гостиницу'),
    ('pension', u'Санаторий'),
]

TYPE_REALTY_NAME = {
    'flat': u'Квартира',
    'room': u'Комната',
    'house': u'Дом',
    'hostel': u'Хостел',
    'mini': u'Мини-отель',
    'hotel': u'Гостиница',
    'pension': u'Санаторий',
}

TYPE_REALTY_LIST = [x[0] for x in TYPE_REALTY]

PLACE = [
    ('city', u'В городе'),
    ('coast', u'На побережье'),
    ('town', u'В поселке'),
    ('river', u'У реки'),
    ('forest', u'В лесу'),
    ('river', u'На берегу озера'),
    ('village', u'В сельской местности'),
    ('mountain', u'В горах'),
]

TYPE_BEACH = [
    ('pebble', u'Галечный'),
    ('sand', u'Песчаный'),
    ('concrete', u'Бетонный'),
]

MOVE = [
    ('afoot', u'Пешком'),
    ('transport', u'На транспорте'),
]

STATUS = [
    ('owner', u'Собственник'),
    ('agency', u'Агентство'),
]

ROOM_COUNT = [
    (0, u'Студия'),
    (1, u'1'),
    (2, u'2'),
    (3, u'3'),
    (4, u'4'),
    (5, u'5 и больше'),
]

TYPE_HOUSE = [
    ('panel', u'Панельный'),
    ('monolithic', u'Монолитный'),
    ('monolith-brick', u'Монолитно-кирпичный'),
    ('modular', u'Блочный'),
    ('brick', u'Кирпичный'),
    ('wood', u'Деревянный'),
]

REPAIR = [
    ('cosmetic', u'Косметический'),
    ('euro', u'Евро'),
    ('design', u'Дизайнерский'),
]

SHOWER = [
    ('number', u'В номере'),
    ('floor', u'На этаже'),
]

WC = [
    ('number', u'В номере'),
    ('floor', u'На этаже'),
]

COOKER = [
    ('gas', u'Газовая'),
    ('electric', u'Электрическая'),
]

TYPE_BED = [
    ('single', u'Односпальная'),
    ('double', u'Двуспальная'),
]

PUBLISHED, UNPUBLISHED = 0, 1
STATUS_BOARD = {
    PUBLISHED: u'Опубликовано',
    UNPUBLISHED: u'Скрыто',
}

MAX_FILE_SIZE = getattr(settings, 'MAX_FILE_SIZE_UPLOAD', 0)
if MAX_FILE_SIZE:
    FILE_SIZE_HELP_TEXT = u'Максимальный размер загружаемого файла не должен превышать {filesize}МБ.'.format(filesize=MAX_FILE_SIZE)
else:
    FILE_SIZE_HELP_TEXT = ''


class City(Site):

    city_name = models.CharField(u'город', max_length=255)
    where = models.CharField(u'в городе', max_length=255)
    head_verification = models.TextField(u'head meta теги', blank=True)
    metro = models.BooleanField(u'метро', default=False)

    class Meta:

        verbose_name = u'город'
        verbose_name_plural = u'города'
        ordering = ['city_name']

    def __unicode__(self):
        return self.city_name


class AddressMixin(models.Model):

    city = models.ForeignKey(City, verbose_name=u'город', null=True, blank=True)
    street = models.CharField(u'адрес', max_length=255)
    place = models.CharField(u'месторасположение', choices=PLACE, max_length=255, default='city', null=True, blank=True)
    type_beach = models.CharField(u'тип пляжа', choices=TYPE_BEACH, max_length=255, blank=True)
    metro = models.PositiveIntegerField(u'до метро мин.', null=True, blank=True)
    beach = models.PositiveIntegerField(u'до пляжа мин.', null=True, blank=True)
    move_metro = models.CharField(u'как', choices=MOVE, max_length=255, default='afoot', null=True, blank=True)
    move_beach = models.CharField(u'как', choices=MOVE, max_length=255, default='afoot', null=True, blank=True)
    landmark = models.TextField(u'как добраться', blank=True, help_text=u'Опишите как добраться до места. Обозначьте местные ориентиры. Укажите с какой стороны вход в здание.')

    class Meta:

        abstract = True

    @property
    def address(self):
        return u'{city}, {street}'.format(city=self.city, street=self.street)


class ContactMixin(models.Model):

    status = models.CharField(u'ваш статус', choices=STATUS, max_length=255, default='owner')
    phone = models.CharField(u'моб. телефон', max_length=255)
    contact_name = models.CharField(u'контактное лицо', max_length=255, blank=True)
    email = models.CharField(u'контактный E-mail', max_length=255, blank=True, help_text=u'Будет опубликован')

    class Meta:

        abstract = True


class Board(AddressMixin, ContactMixin):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_%(app_label)s', null=True, blank=True)
    site = models.ForeignKey(Site, related_name='%(class)s_%(app_label)s', null=True, blank=True)
    type_realty = models.CharField(u'тип недвижимости который вы хотите сдать', db_index=True, choices=TYPE_REALTY, max_length=255, default='flat')
    name = models.CharField(u'название или рекламная фраза', max_length=255, help_text=u'Например: Номер с видом на море')
    text = models.TextField(u'описание объявления', blank=True)
    published = models.BooleanField(u'включено', db_index=True, default=True)
    image_main = models.ImageField(u'главная картинка', upload_to='image', null=True, blank=True)

    objects = BoardManager()

    class Meta:

        verbose_name = u'объявление'
        verbose_name_plural = u'объявления'
        ordering = ['-pk']

    def __unicode__(self):
        return self.name

    def get_image_main(self):

        if bool(self.image_main):
            return self.image_main
        else:
            return settings.BLANK_IMAGE

    @property
    def realty(self):
        return getattr(self, self.type_realty)

    @property
    def type_realty_name(self):
        return TYPE_REALTY_NAME.get(self.type_realty, '')

    @property
    def sleep(self):

        sleep = ''

        type_realty = self.realty

        if type_realty is not None:

            count = str(type_realty.sleep)
            last = count[-1:]

            sleep = u'%s {name}' % count
            last = int(last)

            if last <= 0 or (last >= 5 and last <= 9):
                sleep = sleep.format(name=u'спальных мест')
            elif last == 1:
                sleep = sleep.format(name=u'спальное место')
            elif last >= 2 and last <= 4:
                sleep = sleep.format(name=u'спальных места')

        return sleep

    @property
    def status_board(self):

        if self.published:
            return STATUS_BOARD.get(PUBLISHED, '')
        else:
            return STATUS_BOARD.get(UNPUBLISHED, '')

    @models.permalink
    def get_absolute_url(self):

        return 'board_detail', [self.type_realty, self.pk]

    def get_url(self):

        return u'http://' + unicode(self.site) + reverse('board_detail', args=[self.type_realty, self.pk])

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super(Board, self).save(*args, **kwargs)


class Image(models.Model):

    board = models.ForeignKey(Board, related_name='%(class)s', null=True, blank=True)
    image = models.ImageField(u'картинка', upload_to=upload_dir_class_name, null=True, blank=True, validators=[max_file_size_validator], help_text=FILE_SIZE_HELP_TEXT)
    name = models.CharField(u'подпись', max_length=255, blank=True)
    main = models.BooleanField(u'главная', db_index=True, default=False)
    hash_image = models.CharField(u'хеш', max_length=255, blank=True)
    order = models.IntegerField(u'позиция', null=True, blank=True, default=0)

    objects = ImageManager()

    class Meta:

        verbose_name = u'изображение'
        verbose_name_plural = u'изображения'
        ordering = ['order', 'pk']

    def __unicode__(self):

        if self.name:
            return self.name
        else:
            return unicode(self.pk)


class Price(models.Model):

    board = models.OneToOneField(Board, related_name='%(class)s', null=True, blank=True)
    price = models.PositiveIntegerField(u'цена за сутки проживания', validators=[MinValueValidator(100)])
    prepay = models.PositiveIntegerField(u'предоплата', null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    clearing = models.BooleanField(u'возможен безналичный расчет')
    agreement = models.BooleanField(u'заселение по договору')
    documents = models.BooleanField(u'отчетные документы')
    checkin = models.CharField(u'время заезда', max_length=255, blank=True)
    checkout = models.CharField(u'расчетный час', max_length=255, blank=True)
    additional_bed = models.PositiveIntegerField(u'стоимость доп. спального места', null=True, blank=True)

    class Meta:

        verbose_name = u'цена'
        verbose_name_plural = u'цены'

    def __unicode__(self):
        return unicode(self.price)


class Discount(models.Model):

    board = models.ForeignKey(Board, related_name='%(class)s', null=True, blank=True)
    stay = models.PositiveIntegerField(u'срок проживания от', null=True, blank=True)
    discount = models.PositiveIntegerField(u'скидка', null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    conditions = models.CharField(u'условия', max_length=255, blank=True)

    class Meta:

        verbose_name = u'скидка'
        verbose_name_plural = u'скидки'
        ordering = ['discount']

    def __unicode__(self):
        return unicode(self.discount) + u'%'

    @property
    def stay_view(self):

        stay = ''

        if self.stay is not None:

            stay = str(self.stay)
            last = stay[-1:]
            stay = u'при проживании от %s {name}.' % stay

            if last == 1:
                stay = stay.format(name=u'дня')
            else:
                stay = stay.format(name=u'дней')

        return stay


class PriceMonth(models.Model):

    board = models.ForeignKey(Board, related_name='%(class)s', null=True, blank=True)
    price = models.PositiveIntegerField(u'цена за сутки', db_index=True, null=True, blank=True, validators=[MinValueValidator(100)])
    from_date = models.CharField(u'с', max_length=255, blank=True)
    to_date = models.CharField(u'по', max_length=255, blank=True)

    def __unicode__(self):
        return unicode(self.price)


class OwnPrice(models.Model):

    board = models.ForeignKey(Board, related_name='%(class)s', null=True, blank=True)
    price = models.FileField(u'прайс', upload_to=upload_dir_class_name, blank=True, null=True, validators=[max_file_size_validator], help_text=FILE_SIZE_HELP_TEXT)

    def __unicode__(self):
        return unicode(self.price)


class OverallMixin(models.Model):

    board = models.OneToOneField(Board, related_name='%(class)s', null=True, blank=True)
    floors = models.PositiveIntegerField(u'этажность здания', null=True, blank=True)
    sleep = models.PositiveIntegerField(u'кол-во спальных мест', db_index=True)
    balcony = models.BooleanField(u'балкон')
    repair = models.CharField(u'ремонт', choices=REPAIR, max_length=255, null=True, blank=True)

    class Meta:

        abstract = True


class FloorMixin(models.Model):

    floor_number = models.PositiveIntegerField(u'этаж')
    elevator = models.BooleanField(u'есть лифт')

    class Meta:

        abstract = True


class SpaceMixin(models.Model):

    total_space = models.DecimalField(u'общая площадь м²', db_index=True, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    living_space = models.DecimalField(u'жилая площадь м²', db_index=True, max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    kitchen = models.DecimalField(u'кухня м²', max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    class Meta:

        abstract = True


class RoomMixin(models.Model):

    count = models.PositiveIntegerField(u'общее кол-во комнат', choices=ROOM_COUNT, db_index=True, null=True, blank=True)

    class Meta:

        abstract = True


class HouseMixin(models.Model):

    type_house = models.CharField(u'тип дома', choices=TYPE_HOUSE, max_length=255, null=True, blank=True)
    housing_estate = models.CharField(u'название ЖК либо микрорайона', max_length=255, blank=True)

    class Meta:

        abstract = True


class NumberMixin(models.Model):

    count_number = models.PositiveIntegerField(u'общее кол-во номеров', null=True, blank=True)
    type_number = models.CharField(u'тип номера', max_length=255, blank=True, help_text=u'Например: Стандарт')

    class Meta:

        abstract = True


class OverallComfortMixin(models.Model):

    type_bed = models.CharField(u'тип кровати', choices=TYPE_BED, max_length=255, blank=True)
    tv = models.BooleanField(u'телевизор')
    phone = models.BooleanField(u'телефон')
    conditioner = models.BooleanField(u'кондиционер')
    fan = models.BooleanField(u'вентилятор')
    heater = models.BooleanField(u'водонагреватель')
    linens = models.BooleanField(u'постельное белье')
    washer = models.BooleanField(u'стиральная машина')
    shower_cabine = models.BooleanField(u'душевая кабина')
    table = models.BooleanField(u'стол и стулья')
    cupboard = models.BooleanField(u'шкаф')
    nightstand = models.BooleanField(u'тумбочка')
    mirror = models.BooleanField(u'зеркало')
    iron = models.BooleanField(u'утюг и гладильная доска')
    dishes = models.BooleanField(u'посуда и приборы')
    frig = models.BooleanField(u'холодильник')
    microwave = models.BooleanField(u'микроволновка')
    coffee = models.BooleanField(u'кофемашина')
    kettle = models.BooleanField(u'чайник')
    parking = models.BooleanField(u'парковка')
    protected = models.BooleanField(u'охраняемая территория')
    other_comfort = models.TextField(u'остальные удобства', blank=True)

    class Meta:

        abstract = True

    def get_property(self, fields, prefix=u'<i class="fa fa-check-circle-o"></i> ', postfix=u'<br />'):

        result = ''
        type_realty = self.board.realty

        for x in fields:

            value = getattr(type_realty, x, None)

            if value:
                string_format = u'{prefix}{name}{postfix}'

                if isinstance(value, basestring):
                    string_format = u'{prefix}{name}: {value}{postfix}'

                name = self._meta.get_field(x).verbose_name.capitalize()
                result += string_format.format(prefix=prefix, name=name, value=value, postfix=postfix)

        return mark_safe(result)

    @property
    def comfort(self):

        fields = ['internet', 'frig', 'washer', 'shower_cabine', 'microwave', 'kettle', 'coffee', 'dishes', 'linens', 'fan', 'conditioner', 'phone', 'tv', 'heater', 'table', 'cupboard', 'nightstand', 'mirror', 'iron', 'parking', 'protected']

        return self.get_property(fields)


class RoomComfortMixin(models.Model):

    cooker = models.CharField(u'плита', choices=COOKER, max_length=255, null=True, blank=True)
    internet = models.BooleanField(u'интернет')

    class Meta:

        abstract = True


class HotelComfortMixin(models.Model):

    stars = models.PositiveIntegerField(u'количество звёзд', null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    shower = models.CharField(u'душ', choices=SHOWER, max_length=255, null=True, blank=True)
    wc = models.CharField(u'санузел', choices=WC, max_length=255, null=True, blank=True)
    cleaning = models.CharField(u'уборка в номере', max_length=255, blank=True, help_text=u'Например: Ежедневно')
    bed_linen = models.CharField(u'смена постельного белья', max_length=255, blank=True, help_text=u'Например: Раз в 3 дня')
    terrace = models.BooleanField(u'терраса')
    billiard = models.BooleanField(u'бильярд')
    pool = models.BooleanField(u'бассейн')
    sauna = models.BooleanField(u'сауна')
    solarium = models.BooleanField(u'солярий')
    massage = models.BooleanField(u'массажный кабинет')
    gym = models.BooleanField(u'тренажерный зал')
    restroom = models.BooleanField(u'комната отдыха')
    canteen = models.BooleanField(u'столовая')
    taxi = models.BooleanField(u'услуги такси')
    beach = models.BooleanField(u'собственный пляж')
    excursions = models.BooleanField(u'экскурсии')
    animation = models.BooleanField(u'анимация')
    wifi = models.BooleanField(u'wi-fi в номере')

    class Meta:

        abstract = True

    @property
    def hotel_comfort(self):

        fields = ['cleaning', 'bed_linen', 'beach', 'wifi', 'terrace', 'billiard', 'pool', 'sauna', 'solarium', 'massage', 'gym', 'restroom', 'canteen', 'taxi', 'excursions', 'animation']

        return self.get_property(fields)


class IncludeMixin(models.Model):

    breakfast_incude = models.BooleanField(u'завтрак')
    lunch_incude = models.BooleanField(u'обед')
    dinner_incude = models.BooleanField(u'ужин')
    safe_incude = models.BooleanField(u'сейф')
    fen_incude = models.BooleanField(u'фен')
    bathrobe_incude = models.BooleanField(u'халат')
    sneakers_incude = models.BooleanField(u'тапочки')
    towels_incude = models.BooleanField(u'полотенца')
    minibar_incude = models.BooleanField(u'минибар')
    baggage_incude = models.BooleanField(u'комната для багажа')
    transfer_incude = models.BooleanField(u'трансфер')
    shizlong_incude = models.BooleanField(u'шизлонги')
    additional_incude = models.TextField(u'дополнительно включено в стоимость', blank=True)

    class Meta:

        abstract = True

    @property
    def include(self):

        fields = ['breakfast_incude', 'lunch_incude', 'dinner_incude', 'safe_incude', 'fen_incude', 'bathrobe_incude', 'sneakers_incude', 'towels_incude', 'minibar_incude', 'baggage_incude', 'transfer_incude', 'shizlong_incude']

        return self.get_property(fields, prefix=u'<i class="fa fa-check"></i> ')


class PaidMixin(models.Model):

    safe_paid = models.BooleanField(u'сейф')
    fen_paid = models.BooleanField(u'фен')
    internet_paid = models.BooleanField(u'интернет')
    minibar_paid = models.BooleanField(u'минибар')
    transfer_paid = models.BooleanField(u'трансфер')
    shizlong_paid = models.BooleanField(u'шизлонги')
    additional_paid = models.TextField(u'дополнительные платные услуги', blank=True, help_text=u'Например: Услуги гида')

    @property
    def paid(self):

        fields = ['safe_paid', 'fen_paid', 'internet_paid', 'minibar_paid', 'transfer_paid', 'shizlong_paid']

        return self.get_property(fields, prefix=u'<i class="fa fa-check"></i> ')

    class Meta:

        abstract = True


class NearbyMixin(models.Model):

    stores = models.BooleanField(u'магазины')
    market = models.BooleanField(u'рынок')
    shopping_center = models.BooleanField(u'торговый центр')
    bars = models.BooleanField(u'бары')
    cafe = models.BooleanField(u'кафе')
    restaurants = models.BooleanField(u'рестораны')
    pizzeria = models.BooleanField(u'пиццерия')
    fast_food = models.BooleanField(u'фастфуд')
    salon = models.BooleanField(u'салон красоты')
    nightclub = models.BooleanField(u'ночной клуб')
    spa = models.BooleanField(u'СПА-центр')
    boat_trips = models.BooleanField(u'водные экскурсии')
    bike = models.BooleanField(u'прокат велосипедов')
    attractions = models.BooleanField(u'аттракционы')
    waterpark = models.BooleanField(u'аквапарк')
    museum = models.BooleanField(u'музей')
    theater = models.BooleanField(u'театр')
    cinema = models.BooleanField(u'кинотеатр')
    park = models.BooleanField(u'парк')
    forest = models.BooleanField(u'лес')
    lions = models.TextField(u'местные достопримечательности', blank=True)

    class Meta:

        abstract = True

    @property
    def nearby(self):

        fields = ['stores', 'market', 'shopping_center', 'bars', 'cafe', 'restaurants', 'pizzeria', 'fast_food', 'salon', 'nightclub', 'spa', 'boat_trips', 'bike', 'attractions', 'waterpark', 'museum', 'theater', 'cinema', 'park', 'forest']

        return self.get_property(fields, prefix=u'<i class="fa fa-thumbs-o-up"></i> ')


class ConditionsMixin(models.Model):

    document = models.BooleanField(u'необходим документ, удостоверяющий личность')
    around = models.BooleanField(u'круглосуточное заселение')
    child = models.BooleanField(u'с детьми разрешено')
    animal = models.BooleanField(u'с животными разрешено')
    smoke = models.BooleanField(u'курить разрешено')
    party = models.BooleanField(u'вечеринки разрешены')
    other_condition = models.TextField(u'дополнительные условия заселения', blank=True)

    class Meta:

        abstract = True

    @property
    def condition(self):

        fields = ['document', 'around', 'child', 'animal', 'smoke', 'party']

        return self.get_property(fields, prefix=u'<i class="fa fa-check-square-o"></i> ')


class Flat(OverallMixin, FloorMixin, SpaceMixin, RoomMixin, HouseMixin, OverallComfortMixin, RoomComfortMixin, NearbyMixin, ConditionsMixin):
    pass


class Room(OverallMixin, FloorMixin, RoomMixin, HouseMixin, OverallComfortMixin, RoomComfortMixin, NearbyMixin, ConditionsMixin):

    space = models.DecimalField(u'площадь комнаты м²', max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])


class House(OverallMixin, HouseMixin, RoomMixin, OverallComfortMixin, RoomComfortMixin, NearbyMixin, ConditionsMixin):
    pass


class Hostel(OverallMixin, NumberMixin, OverallComfortMixin, HotelComfortMixin, IncludeMixin, PaidMixin, NearbyMixin, ConditionsMixin):
    pass


class Mini(OverallMixin, NumberMixin, OverallComfortMixin, HotelComfortMixin, IncludeMixin, PaidMixin, NearbyMixin, ConditionsMixin):
    pass


class Hotel(OverallMixin, NumberMixin, OverallComfortMixin, HotelComfortMixin, IncludeMixin, PaidMixin, NearbyMixin, ConditionsMixin):
    pass


class Pension(OverallMixin, NumberMixin, OverallComfortMixin, HotelComfortMixin, IncludeMixin, PaidMixin, NearbyMixin, ConditionsMixin):
    pass
