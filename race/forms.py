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

from common.utils import DateNowInput



pay_way_choices = [('False', 'Наличная'), ('True', 'Безналичная')]
hodki_choices = [('1', '1'), ('1.5', '1.5'), ('2', '2')]
qty_choices = [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]
# empty_choices = [('empty_value', 'empty_label'), ]


class RaceCreateForm(ModelForm):
# ModelChoiceFieldNameLabel
    company = ModelChoiceFieldNameLabel(
        queryset=Companies.objects.all(),
        empty_label=None,
        label_field='name',
        label="Клиент",
        help_text="наименование клиента",
        required=True,
        widget=Select(attrs={
            'size': 2,
            'class': "select2_powered",
            'id': "select2_client"
            })
        )

    contragent = ModelChoiceFieldNameLabel(
        queryset=Contragents.objects.all(),
        label_field='name',
        empty_label=None,
        label="Контрагент",
        help_text="наименование контрагента",
        required=True,
        widget=Select(attrs={
            'size': 2,
            'class': "select2_powered",
            'id': "select2_contragent"
        }))

    place = ModelChoiceFieldNameLabel(
        queryset=Objects.objects.all(),
        label_field='name',
        empty_label=None,
        label="Наименование объекта",
        required=True,
        widget=Select(attrs={
            'size': 2,
            'class': "select2_powered",
            'id': "select2_object"
        }))

    bunker_type = ModelChoiceFieldNameLabel(queryset=BunkerTypes.objects.all(), label="Тип бункеров", empty_label=None, label_field='val')
    bunker_qty = IntegerField(label="Количество", required=True, initial=1, widget=Select(choices=qty_choices, attrs={'size': 1, 'style': 'min-width:6rem;'}))

    cargo_type = ModelChoiceFieldNameLabel(queryset=RaceCargoTypes.objects.all(), label="Тип груза", empty_label=None, label_field='val', widget=Select(attrs={'size': 1, 'style': 'min-width:6rem;'}))

    date_race = DateField(label="Дата рейса", initial=DateNowInput(), widget=RuDateWidget())
    race_type = ModelChoiceFieldNameLabel(queryset=RaceTypes.objects.all(), label="Вид работ", empty_label=None, label_field='val')
    hodkis = DecimalField(label="Ходки", required=False, widget=Select(choices=hodki_choices, attrs={'size': 1, 'style': 'min-width:6rem;'}))

    price = IntegerField(label="Цена", help_text="цена вывоза одного бункера", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices,  widget=RadioSelect())
    summ = DecimalField(label="Сумма", required=True, widget=TextInput(attrs={'size': 1, 'style': 'min-width:6rem;'}))
    recommendation = CharField(label="Примечание к рейсу", required=False, widget=Textarea(attrs={'rows': 2, 'cols': 40}))

    dump = ModelChoiceFieldNameLabel(queryset=Dumps.objects.all(), label="Полигон", empty_label=None, label_field='name')
    dump_pay_type = ChoiceField(label="Плата за полигон", choices=pay_way_choices,  widget=RadioSelect())
    dump_cash = IntegerField(label="Сумма", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    dump_cash_extra = IntegerField(label="Доп. расход", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    dump_cash_comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 10}))
    dump_comment = CharField(label="Примечание к сбросу", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = Races
        fields = ('company', 'contragent', 'place', 'race_type', 'cargo_type',  'price', 'pay_way', 'hodkis', 'date_race', 'summ',
                  'bunker_type', 'bunker_qty', 'dump', 'dump_pay_type', 'dump_cash', 'dump_cash_extra', 'dump_cash_comment', 'dump_comment', )


class RaceUpdateForm(ModelForm):
    bunker_type = ModelChoiceFieldNameLabel(queryset=BunkerTypes.objects.all(), label="Тип бункеров", empty_label=None, label_field='val')
    bunker_qty = IntegerField(label="Количество", required=True, initial=1, widget=Select(choices=qty_choices, attrs={'size': 1, 'style': 'min-width:6rem;'}))

    cargo_type = ModelChoiceFieldNameLabel(queryset=RaceCargoTypes.objects.all(), label="Тип груза", empty_label=None, label_field='val', widget=Select(attrs={'size': 1, 'style': 'min-width:6rem;'}))

    date_race = DateField(label="Дата рейса", initial=DateNowInput(), widget=RuDateWidget())
    race_type = ModelChoiceFieldNameLabel(queryset=RaceTypes.objects.all(), label="Вид работ", empty_label=None, label_field='val')
    hodkis = DecimalField(label="Ходки", required=False, widget=Select(choices=hodki_choices, attrs={'size': 1, 'style': 'min-width:6rem;'}))

    price = IntegerField(label="Цена", help_text="цена вывоза одного бункера", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices,  widget=RadioSelect())
    summ = DecimalField(label="Сумма", required=True, widget=TextInput(attrs={'size': 1, 'style': 'min-width:6rem;'}))
    recommendation = CharField(label="Примечание к рейсу", required=False, widget=Textarea(attrs={'rows': 2, 'cols': 40}))

    dump = ModelChoiceFieldNameLabel(queryset=Dumps.objects.all(), label="Полигон", empty_label=None, label_field='name')
    dump_pay_type = ChoiceField(label="Плата за полигон", choices=pay_way_choices,  widget=RadioSelect())
    dump_cash = IntegerField(label="Сумма", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    dump_cash_extra = IntegerField(label="Доп. расход", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    dump_cash_comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 10}))
    dump_comment = CharField(label="Примечание к сбросу", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = Races
        fields = ('race_type', 'cargo_type', 'price', 'pay_way', 'hodkis', 'date_race', 'summ',
                  'bunker_type', 'bunker_qty', 'dump', 'dump_pay_type', 'dump_cash', 'dump_cash_extra', 'dump_cash_comment', 'dump_comment', )