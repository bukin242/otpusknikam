# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, Template
from django.utils.html import strip_tags
from django.core.management import call_command


TO = [
    'bukin242@yandex.ru',
    'bukin242@gmail.com',
    'otpusknikam@mail.ru'
]


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        call_command('collectstatic', '--noinput')

        context = Context({'url': 'http://otpusknikam.ru/static/email'})
        template = get_template('parse/index.html')
        html = template.render().replace('./', '{{ url }}/')
        body = Template(html).render(context)

        msg = EmailMultiAlternatives('Тест шаблона', strip_tags(body), 'info@otpusknikam.ru', TO)
        msg.attach_alternative(body, 'text/html')
        msg.send()

        print 'send to %s' % TO
