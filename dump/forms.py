# -*- coding: utf8 -*

from re import sub
from django.forms import *
from django.forms.widgets import ChoiceFieldRenderer, RendererMixin, RadioFieldRenderer, RadioChoiceInput, ChoiceInput
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html, html_safe
from django.db.models import Count

from models import *
from common.formfields import *
from common.utils import DateNowInput
from common.forms import RuDateWidget, EmployeeChoiceField, ModelChoiceFieldNameLabel
from person.models import Employies


class TalonsMoveBuyForm(ModelForm):
    type = ChoiceField(label="Тип операции", choices=TalonsFlow.operation_types, initial=0, widget=widgets.HiddenInput())
    employee = EmployeeChoiceField(queryset=Employies.managers.filter(role=4), label="Менеджер по закупкам",  empty_label=None, required=True,)
    employee_group = ChoiceField(label="Группа талонодержателей", choices=TalonsFlow.employee_groups, initial=0, widget=widgets.HiddenInput())
    dump_group = ModelChoiceFieldNameLabel(queryset=DumpGroups.objects.all(), label="Группа полигонов",  label_field="name", empty_label=None, required=True,)
    qty = IntegerField(label="Количество", required=True, min_value=1, initial=0, widget=NumberInput(attrs={'size': 4, 'rel': "price_sum", 'style': 'width: 80px; text-align: right;'}))
    price = DecimalField(label="Цена", decimal_places=0, min_value=1, initial=0, required=True, widget=TextInput(attrs={'size': 6, 'rel': "price_sum", 'style': 'min-width:6rem; text-align: right;'}))
    # sum = DecimalField(label="Стоимость талонов", decimal_places=0, initial=0, required=True, widget=widgets.HiddenInput())
    # sum_paid = DecimalField(label="Сумма оплаты", decimal_places=0, initial=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))

    class Meta:
        model = TalonsFlow
        fields = ('type', 'employee', 'employee_group', 'dump_group', 'qty', 'price', 'comment')


class TalonsMoveBetweenForm(ModelForm):
    dump_group = ModelChoiceFieldNameLabel(queryset=DumpGroups.objects.all(), label="Группа полигонов",  label_field="name", empty_label=None, required=True,)
    employee_from = EmployeeChoiceField(queryset=Employies.objects.filter(role__in=(2,4)), label="Снятие с сотрудника",  empty_label=None, required=True,)
    employee_to = EmployeeChoiceField(queryset=Employies.objects.filter(role__in=(2,4)), label="Передача сотруднику",  empty_label=None, required=True,)
    qty = IntegerField(label="Количество", required=True, min_value=1, initial=0, widget=NumberInput(attrs={'size': 4, 'rel': "price_sum", 'style': 'width: 80px; text-align: right;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))

    class Meta:
        model = TalonsFlow
        fields = ('employee_from', 'employee_to', 'dump_group', 'qty', 'comment')


# class RefuelForm(ModelForm):
#     type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=widgets.HiddenInput())
#     driver = ModelChoiceField(queryset=Employies.drivers.filter(), label="Водитель",  empty_label=None, required=True,)
#     car = ModelChoiceField(queryset=Cars.objects.filter(), label="Автомобиль",  empty_label=None, required=True, )
#     fuel_card = ModelChoiceField(queryset=FuelCards.objects.filter(), widget=widgets.HiddenInput(),  required=False, )
#     amount = IntegerField(label="Кол-во литров", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}), initial=100)
#     summ = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
#     km = IntegerField(label="Километраж", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
#     comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))
#
#     class Meta:
#         model = RefuelsFlow
#         fields = ('type', 'driver', 'car', 'fuel_card', 'amount', 'summ', 'km', 'comment')




