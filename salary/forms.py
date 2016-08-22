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

    class Meta:
        model = SalaryMonthSummary
        fields = ('races_done', 'total_hodkis', 'total_run', 'km_on_hodkis', 'total_amount', 'average_consumption', 'over_run_status', 'over_fuel_status', 'mech_comment', )


