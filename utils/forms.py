# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe


class RequiredMixin(object):

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(RequiredMixin, self).__init__(*args, **kwargs)

        required_label = '<strong class="red">*</strong>'

        for field in self.fields.values():
            if not isinstance(field, forms.BooleanField):
                if field.required and field.label:
                    field.label = mark_safe(unicode(field.label) + required_label)


class HelpTextToPlaceHolderMixin(object):

    def __init__(self, *args, **kwargs):
        super(HelpTextToPlaceHolderMixin, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.help_text:
                field.widget.attrs.update({'placeholder': field.help_text})
                field.help_text = u''


class CustomErrorList(ErrorList):

    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):

        if not self:
            return ''

        return mark_safe('<div class="errorlist">%s</div>' % ''.join('<div class="notice error"><i class="fa fa-warning fa-large"></i> %s</div>' % e for e in self))


class CustomErrorMixin(object):

    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        super(CustomErrorMixin, self).__init__(*args, **kwargs)

        self.error_class = CustomErrorList


class FormMixin(RequiredMixin, HelpTextToPlaceHolderMixin, CustomErrorMixin):
    pass
