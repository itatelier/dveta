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
from contragent.models import Contragents

pay_way_choices = [(False, 'Наличная'), (True, 'Безналичная')]


class AdminItemForm(ModelForm):
    direction_choices = ((0, 'Статья расхода'), (1, 'Статья прихода'))
    direction_type = BooleanField(initial=0, label="Тип направления", widget=RadioSelect( choices=direction_choices),  required=False)
    item_group = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), label_field='name', label="Группа статей", empty_label=None, initial=1)
    name = CharField(label="Наименование статьи", required=True, help_text="Краткое наименование статьи учета")

    class Meta:
        model = DdsItems
        fields = ('item_group', 'name', 'direction_type')


class AccountRefillContragentForm(ModelForm):
    item_groups = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группы статей", empty_label=None, required=False, widget=Select(attrs={"size":8}))
    item = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья учета", empty_label=None, required=True, widget=Select(attrs={"size":8, 'style': "width: 270px;"}))
    company = Select2ChoiceField(
        queryset=Companies.objects.all(),
        label_field='name',
        label="Клиент",
        empty_label=None,
        required=False,
        widget=Select(
                attrs={
                    'class': "select2_powered",
                    'id': "select2_company",
                    'data-url': "/company/api/clients/",
                    'data-field': "name",
                    'data-placeholder': "наименование клиента",
                    'data-minlength': 2
                    }
        ))

    account = ModelChoiceField(queryset=DdsAccounts.objects.all(), label="Счет", required=True, widget=HiddenInput())
    summ = DecimalField(label="Сумма", required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices, initial=False,  widget=RadioSelect())
    comment = CharField(label="Примечание к операции", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = DdsFlow
        fields = ('item', 'account', 'summ', 'pay_way', 'comment')


class AccountRefillEmployeeForm(ModelForm):
    item_groups = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группы статей", empty_label=None, required=False, widget=Select(attrs={"size":8}))
    item = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья учета", empty_label=None, required=True, widget=Select(attrs={"size":8, 'style': "width: 270px;"}))

    employee = Select2ChoiceField(
        queryset=Employies.objects.select_related('person').filter(type=2),
        label_field='person',
        label="Сотрудник",
        empty_label=None,
        required=False,
        widget=Select(
                attrs={
                    'class': "select2_powered",
                    'id': "select2_employee",
                    'data-url': "/persons/api/employies_rest/",
                    'data-field': "person.family_name",
                    'data-placeholder': "фамилия сотрудника",
                    'data-minlength': 2,
                    'data-text_func': 'select2_compose_text'
                    }
        ))

    account = ModelChoiceField(queryset=DdsAccounts.objects.filter(type=4), label="Счет", required=True, widget=HiddenInput())
    summ = DecimalField(label="Сумма", required=True, initial=500, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices, initial=False,  widget=RadioSelect())
    comment = CharField(label="Примечание к операции", initial="Testtt", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = DdsFlow
        fields = ('item', 'account', 'summ', 'pay_way', 'comment')


class DdsOperationForm(ModelForm):
    # Касса
    item_groups = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группы статей", empty_label=None, required=False, widget=Select(attrs={"size":8}))
    item = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья учета", empty_label=None, required=True, widget=Select(attrs={"size":8, 'style': "width: 270px;"}))
    account = ModelChoiceField(queryset=DdsAccounts.objects.filter(type=1), label="Счет", required=True, widget=HiddenInput(attrs={'data-type': 1}), )
    summ = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices, initial=False,  widget=RadioSelect())
    comment = CharField(label="Примечание к операции", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = DdsFlow
        fields = ('item', 'account', 'summ', 'pay_way', 'comment')


class DdsTemplateForm(ModelForm):
    ruquired_choices = [(False, 'Нет'), (True, 'Требуется')]
    visible_choices = [(False, 'Нет'), (True, 'Да')]

    name = CharField(label="Наименование шаблона", required=True, widget=TextInput(attrs={'size': 40}))

    # Статья расхода
    item_groups_out = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группа статей", empty_label=None, required=False, widget=Select(attrs={"rel": "select_group",  'data-combined-id': "id_item_out", "size":8}))
    item_out = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья учета", empty_label=None, required=False, widget=Select(attrs={"size": 8, 'style': "width: 270px;"}))

    # Исходный счет
    account_out = ModelChoiceField(queryset=DdsAccounts.objects.filter(), label="Счет отправления", required=False, widget=HiddenInput(attrs={'data-type': 1}), )
    account_out_required = ChoiceField(label="Операция Расхода в шаблоне", choices=ruquired_choices, initial=False,  widget=RadioSelect(attrs={"rel": "required_switch"}))

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


class DdsOperationAccountFormOut(ModelForm):
    item_groups = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группы статей", empty_label=None, required=False, )
    item = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья операции расхода", empty_label=None, required=False, )
    account = ModelChoiceField(queryset=DdsAccounts.objects.filter(), label="Счет списания", required=False, widget=HiddenInput(attrs={'data-type': 1}), )
    # op_type = BooleanField(initial=False, widget=HiddenInput())

    class Meta:
        model = DdsFlow
        fields = ('item', 'account')


class DdsOperationAccountFormIn(ModelForm):
    item_groups = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), initial=1, label_field='name', label="Группы статей", empty_label=None, required=False, )
    item = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.all(), label_field='name', label="Статья операции прихода", empty_label=None, required=False, )
    account = ModelChoiceField(queryset=DdsAccounts.objects.filter(), label="Счет получения", required=False, widget=HiddenInput(attrs={'data-type': 1}), )
    # op_type = BooleanField(initial=True, widget=HiddenInput())

    class Meta:
        model = DdsFlow
        fields = ('item', 'account')


class DdsOperationDetailsForm(ModelForm):
    summ = DecimalField(label="Сумма", decimal_places=0, required=True, widget=TextInput(attrs={'size': 6, 'style': 'min-width:6rem; text-align: right;'}))
    pay_way = ChoiceField(label="Форма оплаты", choices=pay_way_choices, initial=False,  widget=RadioSelect())
    comment = CharField(label="Примечание к операции", required=False, widget=TextInput(attrs={'size': 40}))

    class Meta:
        model = DdsFlow
        fields = ('summ', 'pay_way', 'comment')


