# -*- coding: utf8 -*

from django.forms import *
from models import *

from company.models import *
from contragent.models import *
from car.models import *
from person.models import *
from bunker.models import *
from dump.models import *


from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


pay_way_choices = [('1', 'Наличная'), ('2', 'Безналичная')]
# empty_choices = [('empty_value', 'empty_label'), ]


class RaceCreateForm(ModelForm):
# ModelChoiceFieldNameLabel
    company = ModelChoiceFieldNameLabel(
        queryset=Companies.objects.all(),
        label_field='name',
        label="Наименование",
        help_text="наименование клиента",
        # label_field="name",
        required=True,
        widget=Select(attrs={
            'size': 2,
            'class': "select2_powered",
            'id': "select2_client"
            })
        )

    contragent = ModelChoiceFieldNoOpt(
        queryset=Contragents.objects.all(),
        label="Наименование",
        help_text="наименование контрагента",
        required=True,
        widget=Select(attrs={
            'size': 2,
            'class': "select2_powered",
            'id': "select2_contragent"
        }))

    object = ModelChoiceFieldNoOpt(
        queryset=Contragents.objects.all(),
        label="Наименование объекта",
        required=True,
        widget=Select(attrs={
            'size': 2,
            'class': "select2_powered",
            'id': "select2_object"
        }))


    race_type = ModelChoiceFieldNameLabel(queryset=RaceTypes.objects.all(), label="Вид работ", empty_label=None, label_field='val')
    cargo_type = ModelChoiceFieldNameLabel(queryset=RaceCargoTypes.objects.all(), label="Тип груза", empty_label=None, label_field='val')

    price = IntegerField(label="Цена", help_text="цена вывза одного бункера", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices,  widget=RadioSelect())
    hodkis = IntegerField(label="Ходки", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    bunker_type = ModelChoiceFieldNameLabel(queryset=BunkerTypes.objects.all(), label="Тип бункеров", empty_label=None, label_field='type')
    bunker_qty = IntegerField(label="Количество", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    dump = ModelChoiceFieldNameLabel(queryset=Dumps.objects.all(), label="Полигон", empty_label=None, label_field='name')
    dump_pay_type = BooleanField(label="Плата за полигон",)
    cash = IntegerField(label="Сумма", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    cash_extra = IntegerField(label="Доп. расход", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    dump_cash_comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 40}))
    dump_comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = Races
        fields = ('company', 'contragent', 'race_type', 'cargo_type', 'object', 'price', 'pay_way', 'hodkis',
                  'bunker_type', 'bunker_qty', 'dump', 'dump_pay_type', 'cash', 'cash_extra', 'dump_cash_comment', 'dump_comment', )

