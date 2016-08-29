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

import logging
log = logging.getLogger('django')


class SalaryMechCheckForm(ModelForm):
    over_run_status_choices = [(False, 'Норма'), (True, 'Перерасход')]
    over_fuel_status_choices = [(False, 'Норма'), (True, 'Перерасход')]

    races_done = IntegerField(label="Выполнено рейсов", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    total_hodkis = DecimalField(label="Засчитано ходок", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    total_run = IntegerField(label="Общий пробег", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    km_on_hodkis = DecimalField(label="КМ на Ходку", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    total_amount = DecimalField(label="Расход топлива", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    average_consumption = DecimalField(label="Расход на 100км", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    over_run_status = ChoiceField(label="Оценка пробега", choices=over_run_status_choices, initial=False, widget=widgets.RadioSelect())
    over_fuel_status = ChoiceField(label="Оценка расхода топлива", choices=over_fuel_status_choices, initial=False, widget=widgets.RadioSelect())
    mech_comment = CharField(label="Примечание механика", required=False, widget=TextInput(attrs={'size': 50}))
    check_status = IntegerField(required=False,widget=HiddenInput())

    class Meta:
        model = SalaryMonthSummary
        fields = ('races_done', 'total_hodkis', 'total_run', 'km_on_hodkis', 'total_amount', 'average_consumption', 'over_run_status', 'over_fuel_status', 'mech_comment', 'check_status')


class SalaryOperationCreateForm(ModelForm):
    # TODO: Добавить валидацию даты - дата не может быть ранее закрытого периода

    year_choices = [(2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'), ]
    month_choices = [(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь'), ]

    year = ChoiceField(label="Год", choices=year_choices, required=True, widget=Select(attrs={'style': 'min-width:6rem; text-align: center;'}))
    month = ChoiceField(label="Месяц", choices=month_choices, required=True, widget=Select(attrs={'style': 'min-width:6rem; text-align: center;'}))
    sum = DecimalField(label="Сумма", decimal_places=1, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))
    operation_type = ChoiceField(label="Тип начисления", choices=SalaryOperationNames.operation_types, required=True, widget=Select())
    operation_name = ModelChoiceField(label="Наименование операции", empty_label=None, queryset=SalaryOperationNames.objects.all(), required=True, widget=Select())
    employee = ModelChoiceField(label="Сотрудник", queryset=Employies.objects.select_related('person'), empty_label=None)

    def __init__(self, operation_type=None, employee=None, year=None, month=None, *args, **kwargs):
        super(SalaryOperationCreateForm, self).__init__(*args, **kwargs)
        if year and month:
            self.fields['year'].widget = widgets.HiddenInput()
            self.fields['year'].initial = year
            self.fields['month'].widget = widgets.HiddenInput()
            self.fields['month'].initial = month
        if operation_type:
            self.fields['operation_type'].widget = widgets.HiddenInput()
            self.fields['operation_type'].initial = operation_type
            self.fields['operation_name'].queryset = SalaryOperationNames.objects.filter(group=operation_type)
        if employee:
            self.fields['employee'].widget = widgets.HiddenInput()
            self.fields['employee'].initial = employee

    class Meta:
        model = SalaryFlow
        fields = ('sum', 'comment', 'year', 'month', 'operation_type', 'operation_name', 'employee')
