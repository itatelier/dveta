# -*- coding: utf8 -*

import re
from django.utils import formats
from decimal import Decimal, DecimalException
from django.utils.encoding import smart_text
from django.forms import DateTimeField, ValidationError, DecimalField, DateTimeInput, ModelChoiceField, ChoiceField, Field
from django.core import validators
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView, ModelFormMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.http import HttpResponseRedirect
from django.forms.widgets import RadioSelect
from django.forms.models import ModelChoiceIterator
from django.utils.safestring import mark_safe

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
    form_classes = None

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

        return dict(
            [(classname, params['formclass'](**self.get_form_kwargs(classname))) for classname, params in self.formconf.items()])

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

    def get_context_data(self, **kwargs):
        if 'forms' not in kwargs:
            kwargs['forms'] = self.get_forms()
        if 'view' not in kwargs:
            kwargs['view'] = self
        return kwargs


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
        kwargs['attrs'] = {'pattern': '\d{2}-\d{2}-\d{4}', 'size': 16, 'maxlength': 16}
        kwargs['format'] = '%d-%m-%Y'
        super(RuDateWidget, self).__init__(*args, **kwargs)


class RadioRendererSimple(RadioSelect.renderer):
    def render(self):
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


def replace_modelchoicesfields_data(form, fields):
    # Удаляем queryset из перечисленных полей, что бы генератор не поставил для Select'a всю таблицу из БД.
    # вместо QuerySet добавляем Choices с единичной записью
    for field in fields:
        form.fields[field].queryset = form.fields[field].queryset.none()
        field_data_object = form.cleaned_data.get(str(field), None)
        if field_data_object:
            field_data_object = form.cleaned_data[field]
            form.fields[field].choices = [(field_data_object.id, field_data_object.name), ]
        else:
            form.fields[field].choices = [('', ''), ]
    return form


def none_modelchoicesfields_querysets(form, fields):
    # Для перечисленных полей устанавливаем queryset None
    for field in fields:
        form.base_fields[field].queryset = form.base_fields[field].queryset.none()
    return form


class Select2ChoiceField(ModelChoiceFieldNameLabel):

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            key = self.to_field_name or 'pk'
            obj = self.queryset.get(**{key: value})
        except (ValueError, TypeError, self.queryset.model.DoesNotExist):
            raise ValidationError(u"Значение поля [%s] не найдено в базе" % value, code='invalid_choice')
        return value

    def validate(self, value):
        return Field.validate(self, value)

    def _get_choices(self):
        # If self._choices is set, then somebody must have manually set
        # the property self.choices. In this case, just return self._choices.
        if hasattr(self, '_choices'):
            return self._choices
        #log.info("--- self.value=%s" % self.value())

        # choices2 = ((22, 44), (66, 77))
        # from company.models import *
        # obj = Companies.objects.get(pk=29)
        choices = [("33", "44")]
        # Otherwise, execute the QuerySet in self.queryset to determine the
        # choices dynamically. Return a fresh ModelChoiceIterator that has not been
        # consumed. Note that we're instantiating a new ModelChoiceIterator *each*
        # time _get_choices() is called (and, thus, each time self.choices is
        # accessed) so that we can ensure the QuerySet has not been consumed. This
        # construct might look complicated but it allows for lazy evaluation of
        # the queryset.
        return ModelChoiceIterator(self)
        # return choices

    def _get_queryset(self):
        return self._queryset

    def _set_queryset(self, queryset):
        self._queryset = queryset
        self.widget.choices = self._get_choices()

    queryset = property(_get_queryset, _set_queryset)


class SubsetModelChoiceIterator(ModelChoiceIterator):

    def __init__(self, field):
        self.field = field
        self.queryset = field.subset_queryset


class SubsetModelChoiceField(ModelChoiceField):
    """
    This is just like a ModelChoiceField, but only a subset of the full
    queryset will be displayed as choices.
    """

    def __init__(self, subset_queryset, *args, **kwargs):
        self.subset_queryset = subset_queryset
        super(SubsetModelChoiceField, self).__init__(*args, **kwargs)

    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices

        return SubsetModelChoiceIterator(self)
    choices = property(_get_choices, ChoiceField._set_choices)

    def _get_subset_queryset(self):
        return self._subset_queryset

    def _set_subset_queryset(self, queryset):
        self._subset_queryset = queryset
        self.widget.choices = self.choices