# -*- coding: utf8 -*

from django.forms import *
from models import *

from company.models import *
from car.models import *

from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class RaceCreateForm(ModelForm):
    car = ModelChoiceFieldNameLabel(queryset=Cars.objects.all(), label="Модель авто", empty_label=None)
    driver = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)

    company = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
    contragent = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)

    race_type = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
    cargo_type = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
    object = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)

    price = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    summ = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    pay_way_choices = [('1', 'Наличная'), ('2', 'Безналичная')]
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices,  widget=RadioSelect())

    hodkis = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    bunker_type = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
    bunker_qty = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    dump = ModelChoiceFieldNameLabel(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None, label_field='name')
    dump_pay_type = BooleanField()
    cash = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    cash_extra = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    class Meta:
        model = Races
        fields = ('company', 'contragent', 'race_type', 'cargo_type', 'object', 'price', 'summ', 'pay_way_choices',
                  'pay_way', 'hodkis', 'bunker_type', 'bunker_qty', 'dump', 'dump_pay_type', 'cash', 'cash_extra')

