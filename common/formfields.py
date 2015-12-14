# -*- coding: utf8 -*

from django.forms import *
from django.core import validators

# from rendering input
from django.utils.encoding import force_text
from django.forms.utils import flatatt
from django.utils.html import format_html


class EmailInput(Field):
    input_type = 'email'


class HTML5Input(TextInput):

    def __init__(self, type, attrs):
        self.input_type = type
        self.css_classes = None
        super(HTML5Input, self).__init__(attrs)

    # def render(self, name, value, attrs=None):
    #     if value is None:
    #         value = ''
    #     final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    #     if value != '':
    #         # Only add the 'value' attribute if a value is non-empty.
    #         final_attrs['value'] = force_text(self._format_value(value))
    #     raw_html = '<div class="input_block'+final_attrs['class']+'">' + "\n" + format_html('<input{} />', flatatt(final_attrs)) + "</div>"
    #     return raw_html


class AMarkField(forms.Field):
    default_error_messages = {
        'not_an_a': u'you can only input A here! damn!',
    }

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        return value

    def validate(self, value):
        if value != 'A':
            raise ValidationError(self.error_messages['not_an_a'])