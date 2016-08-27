# -*- coding: utf8 -*

from re import sub
from django.forms import *
from django.forms.widgets import ChoiceFieldRenderer, RendererMixin, RadioFieldRenderer, RadioChoiceInput, ChoiceInput
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html, html_safe
from django.db.models import Count
from datetime import datetime, timedelta


from models import *
from common.forms import *
from common.formfields import *
from company.models import Companies
from car.models import Cars
from contragent.models import Contragents

refuel_types_choices = [(0, 'Карта'), (1, 'Наличные'), (2, 'Талон'), (3, 'База ДТ')]


class RefuelForm(ModelForm):
    date_refuel = DateTimeField(label="Дата заправки", required=False, input_formats=['%d-%m-%Y %H:%M:%S'], widget=widgets.HiddenInput())
    type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=widgets.HiddenInput())
    driver = DriverChoiceField(queryset=Employies.drivers.filter(), label="Водитель",  empty_label=None, required=True,)
    car = ModelChoiceField(queryset=Cars.objects.filter(), label="Автомобиль",  empty_label=None, required=True, )
    fuel_card = ModelChoiceField(label="Топливная карта", queryset=FuelCards.objects.filter(), widget=widgets.HiddenInput(),  required=False, )
    amount = IntegerField(label="Кол-во литров", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}), initial=100)
    sum = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    km = IntegerField(label="Километраж", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))

    def __init__(self, car=None, driver=None, type=None, later_add=None, fuel_card=None, *args, **kwargs):
        super(RefuelForm, self).__init__(*args, **kwargs)
        if car:
            self.fields['car'].widget = widgets.HiddenInput()
            self.fields['car'].initial = car
        if driver:
            self.fields['driver'].widget = widgets.HiddenInput()
            self.fields['driver'].initial = driver
        if type:
            self.fields['type'].widget = widgets.HiddenInput()
            self.fields['type'].initial = type
        if type and int(type) == 0:
            self.fields['sum'].widget = widgets.HiddenInput()
            self.fields['fuel_card'].initial = fuel_card
        if later_add and int(later_add) == 1:
            self.fields['date_refuel'].widget = RuDateWidget()
            self.fields['date_refuel'].initial = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    class Meta:
        model = RefuelsFlow
        fields = ('date_refuel', 'type', 'driver', 'car', 'fuel_card', 'amount', 'sum', 'km', 'comment')


class RunCheckForm(ModelForm):
    type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=widgets.HiddenInput())
    driver = ModelChoiceField(queryset=Employies.drivers.filter(), label="Водитель",  empty_label=None, required=True,)
    car = ModelChoiceField(queryset=Cars.objects.filter(), label="Автомобиль",  empty_label=None, required=True, )
    km = IntegerField(label="Километраж", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: center;'}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 50}))

    class Meta:
        model = CarRunCheckFlow
        fields = ('driver', 'car', 'km', 'comment')
