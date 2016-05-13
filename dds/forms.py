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


class AdminItemForm(ModelForm):
    direction_choices = ((0, 'Статья расхода'), (1, 'Статья прихода'))
    direction_type = BooleanField(initial=0, label="Тип направления", widget=RadioSelect( choices=direction_choices),  required=False)
    item_group = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), label_field='name', label="Группа статей", empty_label=None, initial=1)
    name = CharField(label="Наименование статьи", required=True, help_text="Краткое наименование статьи учета")

    class Meta:
        model = DdsItems
        fields = ('item_group', 'name', 'direction_type')


class AccountRefillForm(ModelForm):
    active_tab = CharField(required=False, widget=HiddenInput())

    dds_item = ModelChoiceFieldNameLabel(queryset=DdsItems.objects.filter(direction_type=True), label_field='name', label="Статья учета", empty_label=None, required=True)
    company = Select2ChoiceField(
        queryset=Companies.objects.all(),
        label_field='name',
        label="Клиент",
        empty_label=None,
        required=True,
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

    contragent = Select2ChoiceField(
        queryset=Contragents.objects.all(),
        required=False,
        label_field='name',
        empty_label=None,
        label="Контрагент",
        widget=Select(attrs={
            'class': "select2_powered",
            'id': "select2_contragent",
            'data-url': "/contragents/api/contragents_list/",
            'data-field': "name",
            'data-placeholder': "наименование контрагента",
            'data-filter_field': 'company',
            'data-filter_value': '',
            }
        )
    )
    account = ModelChoiceField(queryset=DdsAccounts.objects.all(), label="Счет", required=True, widget=HiddenInput())


    class Meta:
        model = DdsFlow
        fields = ('dds_item', 'account' )

