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

    over_run_status = ChoiceField(label="Оценка пробега", choices=over_run_status_choices, initial=False, widget=widgets.RadioSelect())
    over_fuel_status = ChoiceField(label="Оценка расхода топлива", choices=over_fuel_status_choices, initial=False, widget=widgets.RadioSelect())
    fuel_comment = CharField(label="Примечание по топливу", required=False, widget=TextInput(attrs={'size': 50}))
    run_comment = CharField(label="Примечание по пробегу", required=False, widget=TextInput(attrs={'size': 50}))
    check_status = IntegerField(required=False, widget=HiddenInput(), initial=0)

    class Meta:
        model = SalaryMonthSummary
        fields = ('over_run_status', 'over_fuel_status', 'fuel_comment', 'run_comment', 'check_status')


class SalaryRaceStatsForm(ModelForm):

    races_done = IntegerField(required=True, widget=HiddenInput())
    total_hodkis = DecimalField(required=True, widget=HiddenInput())
    total_run = IntegerField(required=True, widget=HiddenInput())
    km_on_hodkis = DecimalField(decimal_places=2, required=True, widget=HiddenInput())
    total_amount = DecimalField(decimal_places=2, required=True, widget=HiddenInput())

    class Meta:
        model = SalaryMonthSummary
        fields = ('races_done', 'total_hodkis', 'total_run', 'km_on_hodkis', 'total_amount', 'over_run_status', 'over_fuel_status', 'fuel_comment', 'run_comment', 'check_status')


class SalaryOfficeCheckForm(ModelForm):
    acr_mobile_days = CharField(label="Дней" ,required=True, widget=HiddenInput())
    acr_basehouse_rent_days = IntegerField(label="Дней", required=True, widget=HiddenInput())
    office_comment = CharField(label="Примечание к проверке офисом", required=False, widget=TextInput(attrs={'size': 50}))

    class Meta:
        model = SalaryMonthSummary
        fields = ('acr_mobile_days', 'acr_basehouse_rent_days', 'check_status', 'office_comment')


class SalaryTopCheckForm(ModelForm):
    top_comment = CharField(label="Примечание к проверке руководителем", required=False, widget=TextInput(attrs={'size': 50}))

    class Meta:
        model = SalaryMonthSummary
        fields = ('check_status', 'top_comment')

    # def __init__(self, month_days=None, *args, **kwargs):
    #     super(SalaryOfficeCheckForm, self).__init__(*args, **kwargs)
    #     if month_days:
    #         self.fields['acr_mobile_days'].widget = widgets.NumberInput(attrs={'min': 1, 'max': month_days, 'size': 2, 'style': 'min-width:6rem; text-align: center;'})
    #         self.fields['acr_mobile_days'].initial = month_days
    #         self.fields['acr_basehouse_rent_days'].widget = widgets.NumberInput(attrs={'min': 1, 'max': month_days, 'size': 2, 'style': 'min-width:6rem; text-align: center;'})
    #         self.fields['acr_basehouse_rent_days'].initial = month_days

# class SalaryMechCheckForm(ModelForm):


class SalaryOperationCreateForm(ModelForm):
    # TODO: Добавить валидацию даты - дата не может быть ранее закрытого периода

    year_choices = [(2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'), ]
    month_choices = [(1, 'Январь'), (2, 'Февраль'), (3, 'Март'), (4, 'Апрель'), (5, 'Май'), (6, 'Июнь'), (7, 'Июль'), (8, 'Август'), (9, 'Сентябрь'), (10, 'Октябрь'), (11, 'Ноябрь'), (12, 'Декабрь'), ]

    year = ChoiceField(label="Год", choices=year_choices, required=True, widget=Select(attrs={'style': 'min-width:6rem; text-align: center;'}))
    month = ChoiceField(label="Месяц", choices=month_choices, required=True, widget=Select(attrs={'style': 'min-width:6rem; text-align: center;'}))
    sum = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))
    operation_type = ModelChoiceField(label="Тип начисления", queryset=SalaryOperationTypes.objects.all(), required=True, widget=Select())
    operation_name = ModelChoiceField(label="Наименование операции", empty_label=None, queryset=SalaryOperationNames.objects.all(), required=True, widget=Select())
    operation_direction = BooleanField(required=False, initial=False, widget=HiddenInput())
    employee = ModelChoiceField(label="Сотрудник", queryset=Employies.objects.select_related('person'), empty_label=None)

    def __init__(self, operation_type=None, operation_direction=None, employee=None, year=None, month=None, *args, **kwargs):
        super(SalaryOperationCreateForm, self).__init__(*args, **kwargs)
        if year and month:
            self.fields['year'].widget = widgets.HiddenInput()
            self.fields['year'].initial = year
            self.fields['month'].widget = widgets.HiddenInput()
            self.fields['month'].initial = month
        if operation_type:
            self.fields['operation_type'].widget = widgets.HiddenInput()
            self.fields['operation_type'].initial = operation_type
            self.fields['operation_name'].queryset = SalaryOperationNames.objects.filter(type=operation_type)
        if employee:
            self.fields['employee'].widget = widgets.HiddenInput()
            self.fields['employee'].initial = employee
        if operation_direction:
            self.fields['operation_direction'].initial = True

    def clean(self):
        # Если направление операции == 0, добавляем отрицательный знак к сумме
        cleaned_data = super(SalaryOperationCreateForm, self).clean()
        direction = cleaned_data.get("operation_direction", '')
        if not direction:
            cleaned_data['sum'] = -(abs(cleaned_data['sum']))
        return cleaned_data

    class Meta:
        model = SalaryFlow
        fields = ('sum', 'comment', 'year', 'month', 'operation_type', 'operation_name', 'employee', 'operation_direction')
