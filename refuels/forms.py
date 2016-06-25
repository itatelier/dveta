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
    type = ChoiceField(label="Тип заправки", choices=refuel_types_choices, initial=0,  widget=RadioSelect())
    driver = ModelChoiceField(queryset=Employies.drivers.filter(), label="Водитель", required=False, widget=HiddenInput(attrs={'data-type': 1}), )
    car = ModelChoiceField(queryset=Cars.objects.filter(), label="Счет получения", required=False, widget=HiddenInput(attrs={'data-type': 1}), )


    driver = models.ForeignKey('person.Employies', null=False, blank=False)
    fuel_card = models.ForeignKey('FuelCards', null=True, blank=True)
    type = models.IntegerField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    summ = models.FloatField(null=False, blank=False)
    km = models.IntegerField(null=False, blank=False)
    comment = models.CharField(max_length=255L, null=True, blank=True)


    name = CharField(label="Наименование шаблона", required=True, widget=TextInput(attrs={'size': 40}))

    # Статья прихода
    item_groups_in = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группа статей", empty_label=None, required=False, widget=Select(attrs={"rel": "select_group", 'data-combined-id': "id_item_in", "size":8}))
    item_in = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья учета", empty_label=None, required=False, widget=Select(attrs={"size": 8, 'style': "width: 270px;"}))

    # Счет получателя
    account_in = ModelChoiceField(queryset=DdsAccounts.objects.filter(), label="Счет получения", required=False, widget=HiddenInput(attrs={'data-type': 1}), )
    account_in_required = ChoiceField(label="Операция Прихода в шаблоне", choices=ruquired_choices, initial=False,  widget=RadioSelect(attrs={"rel": "required_switch"}))

    summ = DecimalField(label="Сумма", decimal_places=0, required=False, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices, initial=False,  widget=RadioSelect())
    comment = CharField(label="Примечание к операции", required=False, widget=TextInput(attrs={'size': 40}))
    group = ModelChoiceFieldNameLabel(label="Группа шаблонов", required=True, queryset=DdsTemplateGroups.objects.all(), label_field='name', empty_label=None,)

    class Meta:
        model = DdsTemplates
        fields = ('name', 'item_groups_out', 'item_out','account_out',
                  'account_out_required', 'item_groups_in', 'item_in', 'account_in', 'account_in_required', 'summ', 'pay_way', 'comment', 'group')

