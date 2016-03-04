# -*- coding: utf8 -*

from django.forms import *
from models import *
from company.models import *
from person.models import *
from object.models import Objects
from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import logging
log = logging.getLogger('django')
from django.db import models


def get_attr_or_null(cls, val):
   val = getattr(cls, val, '')
   return val


class BunkerFlowForm(ModelForm):
    object_out = ModelChoiceFieldNoOpt(
        queryset=Objects.objects.all(),
        label="Исходный объект",
        help_text="объект, с которого переходит бункер",
        label_field="name",
        required=False,
        widget=Select(attrs={
            'size': 10,
            'class': "select2_powered"
        }))

    object_in = ModelChoiceFieldNoOpt(
        queryset=Objects.objects.all(),
        label="Объект назначения",
        help_text="объект на который переходит бункер",
        label_field="name",
        required=False,
        widget=Select(attrs={
            'size': 10,
            'class': "select2_powered",
        }))
    qty = DecimalField(label="Количество", max_digits=10, decimal_places=0, required=True, widget=forms.TextInput(attrs={'size': 6, 'maxlength': 6}))
    bunker_type = ModelChoiceFieldNameLabel(queryset=BunkerTypes.objects.all(), label_field="val", label="Тип бункера", empty_label=None)
    operation_type = ModelChoiceFieldNameLabel(queryset=BunkerOperationTypes.objects.all(), label_field="val",label="Операция", empty_label=None)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(BunkerFlowForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BunkerFlow
        fields = ('object_in', 'object_out', 'qty', 'bunker_type', 'operation_type')

    def clean(self):
        cleaned_data = super(BunkerFlowForm, self).clean()
        qty = cleaned_data.get("qty")
        object_out = cleaned_data['object_out']
        object_in = cleaned_data['object_in']
        bunker_type = cleaned_data['bunker_type']
        operation_type = cleaned_data['operation_type']

        if object_out is None and object_in is None:
            raise forms.ValidationError("Не указаны объекты перемещения.")
        if object_out == object_in:
            raise forms.ValidationError("Исходный объект и объект назначения не могут быть одинаковыми")
        if operation_type in (2, 3, 4, 5) and object_out is None:
            raise forms.ValidationError("Исходный объект для данной операции должен быть указан")
        if operation_type in (1, 2, 3, 4) and object_in is None:
            raise forms.ValidationError("Объект назначения для данной операции должен быть указан")

        # проверка остатков на исходном объекте
        remains = Objects.objects.get(pk=object_out.pk).bunker_remain.get(type=bunker_type).qty
        if operation_type in (2, 3, 4, 5) and remains < qty:
            raise forms.ValidationError("Остаток на объекте меньше указанного количества для перемещения")
        return cleaned_data
