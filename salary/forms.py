# -*- coding: utf8 -*

from re import sub
from django.forms import *
from django.forms.widgets import ChoiceFieldRenderer, RendererMixin, RadioFieldRenderer, RadioChoiceInput, ChoiceInput
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html, html_safe
from django.db.models import Count

from models import *
from common.forms import *
from common.formfields import *
from company.models import Companies
from car.models import Cars
from contragent.models import Contragents


class SalaryMechCheckForm(ModelForm):
    races_done = IntegerField(label="Выполнено рейсов", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    hodkis = DecimalField(label="Засчитано ходок", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    run_km = IntegerField(label="Общий пробег", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    average_consumption = DecimalField(label="Средний расход топлива на 100км", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))

    mech_comment = CharField(label="Примечание механика", required=False, widget=TextInput(attrs={'size': 50}))

#     date_refuel = DateTimeField(label="Дата заправки", required=False, input_formats=['%d-%m-%Y %H:%M:%S'], widget=widgets.HiddenInput())
#     type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=widgets.HiddenInput())
#    driver = DriverChoiceField(queryset=Employies.drivers.filter(), label="Водитель",  empty_label=None, required=True, widget=widgets.HiddenInput())
#     car = ModelChoiceField(queryset=Cars.objects.filter(), label="Автомобиль",  empty_label=None, required=True, )
#     fuel_card = ModelChoiceField(label="Топливная карта", queryset=FuelCards.objects.filter(), widget=widgets.HiddenInput(),  required=False, )
#     amount = IntegerField(label="Кол-во литров", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}), initial=100)
#     sum = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
#     km = IntegerField(label="Километраж", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
#
    # id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    #
    # races_done = models.IntegerField(null=False, blank=False)
    # hodkis = models.IntegerField(null=False, blank=False)
    # run_km = models.IntegerField(null=False, blank=False)
    # average_consumption = models.IntegerField(null=False, blank=False)
    #
    # over_run_status = models.NullBooleanField(null=True, blank=True, default=False)
    # over_fuel_status = models.NullBooleanField(null=True, blank=True, default=False)
    # mech_comment = models.CharField(max_length=255L, null=True, blank=True)
    #
    # over_run_penalty = models.FloatField(null=True, blank=True)
    # over_fuel_penalty = models.FloatField(null=True, blank=True)
#     class Meta:
#         model = RefuelsFlow
#         fields = ('date_refuel', 'type', 'driver', 'car', 'fuel_card', 'amount', 'sum', 'km', 'comment')
#
#
# class RunCheckForm(ModelForm):
#     type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=widgets.HiddenInput())
#     driver = ModelChoiceField(queryset=Employies.drivers.filter(), label="Водитель",  empty_label=None, required=True,)
#     car = ModelChoiceField(queryset=Cars.objects.filter(), label="Автомобиль",  empty_label=None, required=True, )
#     km = IntegerField(label="Километраж", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
#     comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))
#
#     class Meta:
#         model = CarRunCheckFlow
#         fields = ('driver', 'car', 'km', 'comment')
