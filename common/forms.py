# -*- coding: utf8 -*

import re
from django.utils import formats
from decimal import Decimal, DecimalException
from django.utils.encoding import smart_text
from django.forms import DateTimeField, ValidationError, DecimalField, DateTimeInput, ModelChoiceField
from django.core import validators
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView, ModelFormMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.http import HttpResponseRedirect

import logging
log = logging.getLogger('django')


class ModelChoiceFieldNameLabel(ModelChoiceField):
    # Возвращаем только определенное поле из таблицы для вариантов значений Select
    def __init__(self, label_field, *args, **kwargs):
        super(ModelChoiceFieldNameLabel, self).__init__(*args, **kwargs)
        self.label_field = label_field

    def label_from_instance(self, obj ):
        if self.label_field is not None:
            return getattr(obj, self.label_field)


class MultiFormCreate(FormMixin, TemplateResponseMixin, View):
    formconf = None

    def get_form_classes(self):
        form_classes = {}
        for key, params in self.formconf.items():
            form_classes[key] = params.formclass
        return self.form_classes

    def get_initial(self, classname):
        initial = {}
        if 'initial' in self.formconf[classname]:
            initial = self.formconf[classname]['inicial'].copy()
        return initial

    def get_instance(self, classname):
        instance = None
        if 'instance' in self.formconf[classname]:
            instance = self.formconf[classname]['instance']
        return instance

    def get_form_kwargs(self, classname):
        kwargs = {'initial': self.get_initial(classname), 'prefix': classname, 'instance': self.get_instance(classname)}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
                })
        return kwargs

    def get_forms(self):
        # for classname, params in self.formconf.items():
            # log.info("classname: %s, Params: %s" % (classname, params))
        return dict(
            [(classname, params['formclass'](**self.get_form_kwargs(classname))) for classname, params in self.formconf.items()])
            # ''' { classname: SomeCreateForm(**kwargs), } '''

    def get(self, request, *args, **kwargs):
        forms = self.get_forms()
        return self.render_to_response(self.get_context_data(forms=forms))

    def get_success_url(self):
        if self.success_url:
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url


class MultiFormEdit(MultiFormCreate):

    def update_formconf(self, *args, **kwargs):
        return self.formconf

    def get(self, request, *args, **kwargs):
        self.formconf = self.update_formconf(self.formconf, *args, **kwargs)
        forms = self.get_forms()
        return self.render_to_response(self.get_context_data(forms=forms))

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        form_not_valid = None
        for formclass, form in forms.items():
            if not form.is_valid():
                form_not_valid = 1
        if form_not_valid is None:
            for formclass in forms:
                forms[formclass].save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(forms=forms))


class DecimalFieldMix(DecimalField):

    def to_python(self, value):
        if value in validators.EMPTY_VALUES:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
        value = re.sub(r'\s|\tr', '', value)
        value = smart_text(value).strip()
        try:
            value = Decimal(value)
        except DecimalException:
            raise ValidationError(self.error_messages['invalid'])
        return value


class RuDateWidget(DateTimeInput):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'pattern': '\d{2}.\d{2}.\d{4}', 'size': 16, 'maxlength': 16}
        kwargs['format'] = '%d.%m.%Y'
        super(RuDateWidget, self).__init__(*args, **kwargs)

