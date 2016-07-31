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

refuel_types_choices = [(0, 'Карта'), (1, 'Наличные'), (2, 'Талон'), (3, 'База ДТ')]


class RefuelForm(ModelForm):
    type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=widgets.HiddenInput())
    driver = ModelChoiceField(queryset=Employies.drivers.filter(), label="Водитель",  empty_label=None, required=True,)
    car = ModelChoiceField(queryset=Cars.objects.filter(), label="Автомобиль",  empty_label=None, required=True, )
    fuel_card = ModelChoiceField(label="Топливная карта", queryset=FuelCards.objects.filter(), widget=widgets.HiddenInput(),  required=False, )
    amount = IntegerField(label="Кол-во литров", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}), initial=100)
    sum = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    km = IntegerField(label="Километраж", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))

    class Meta:
        model = RefuelsFlow
        fields = ('type', 'driver', 'car', 'fuel_card', 'amount', 'sum', 'km', 'comment')


