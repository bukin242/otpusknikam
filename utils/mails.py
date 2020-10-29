# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.html import strip_tags, linebreaks
import string


def string_to_list(value, separate=','):

    if isinstance(value, basestring):
        value = value.split(separate)
        value = filter(None, value)
        value = map(string.strip, value)

    return value


class TemplateEmailMessage(EmailMultiAlternatives):

    def __init__(self, *args, **kwargs):

        self.template_name = kwargs.pop('template_name', None)
        self.object = kwargs.pop('object', None)
        self.extend_context = kwargs.pop('extend_context', {})
        self.linebreaks = kwargs.pop('linebreaks', True)

        super(TemplateEmailMessage, self).__init__(*args, **kwargs)

        self.reply_to = kwargs.pop('reply_to', self.from_email)

        from_email = string_to_list(self.from_email)
        if from_email:
            self.from_email = from_email[0]

    def send(self, *args, **kwargs):

        if not len(self.body) and self.template_name is not None:

            if self.object is None:
                context_text = {}
            else:
                context_text = {'object': self.object}

            context_text.update(self.extend_context)

            config = getattr(settings, 'CONFIG', {})
            context_text.update({'config': config})

            context = Context(context_text)
            template = get_template(self.template_name)
            body = template.render(context)

        else:
            body = self.body

        if self.linebreaks:
            body = linebreaks(body)

        self.body = strip_tags(body)
        self.attach_alternative(body, 'text/html')

        self.to = string_to_list(self.to)
        self.to = self.to or [settings.DEFAULT_FROM_EMAIL]

        self.reply_to = string_to_list(self.reply_to)

        from_name = getattr(settings, 'DEFAULT_FROM_EMAIL_NAME', '')
        if from_name:
            self.extra_headers = {
                'From': u'%s <%s>' % (from_name, self.from_email, )
            }

        return super(TemplateEmailMessage, self).send(*args, **kwargs)


class CallSendEmailMixin(object):

    def save(self, *args, **kwargs):

        self.object = super(CallSendEmailMixin, self).save(*args, **kwargs)

        if getattr(self, 'send_email', None):
            self.send_email()

        return self.object


class SendEmailMixin(CallSendEmailMixin):

    def __init__(self, *args, **kwargs):
        super(SendEmailMixin, self).__init__(*args, **kwargs)

        self.template_name = getattr(self.Meta, 'send_email_template_name', getattr(self, 'template_name', None))
        self.subject = getattr(self.Meta, 'send_email_subject', getattr(self, 'subject', None))
        self.body = getattr(self.Meta, 'send_email_body', getattr(self, 'body', None))
        self.extend_context = getattr(self.Meta, 'send_email_extend_context', getattr(self, 'extend_context', {}))
        self.reply_to_field = getattr(self.Meta, 'send_email_reply_to_field', getattr(self, 'reply_to_field', None))
        self.reply_to = getattr(self.Meta, 'send_email_reply_to', getattr(self, 'reply_to', None))
        self.to_field = getattr(self.Meta, 'send_email_to_field', getattr(self, 'to_field', None))
        self.to = getattr(self.Meta, 'send_email_to', getattr(self, 'to', None))

    def send_email(self):

        if self.subject:

            message = TemplateEmailMessage()

            if self.body:
                message.body = self.body
            else:
                message.template_name = self.template_name

            message.subject = self.subject
            message.object = self.instance
            message.extend_context = self.extend_context

            if self.reply_to_field:
                message.reply_to = getattr(self.instance, self.reply_to_field)

                if not message.reply_to and self.reply_to:
                    message.reply_to = self.reply_to

            elif self.reply_to:
                message.reply_to = self.reply_to

            if self.to_field:
                message.to = getattr(self.instance, self.to_field)
            elif self.to:
                message.to = self.to

            message.send()
