# -*- coding: utf8 -*

from re import sub
from django.forms import *
from models import *
from common.forms import *
from common.formfields import *

import logging
log = logging.getLogger('django')


class CompanyCreateForm(ModelForm):
    name = CharField(label="Наименование", required=True, help_text="Краткое наименование клента, простое, как \"Утюг\"")
    description = CharField(label="Род деятельности", required=False, help_text="Описание деятельности компании", widget=TextInput(attrs={'placeholder': "Строительство, Юридические услуги", 'size': 50}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 40}))
    attr_source = ModelChoiceFieldNameLabel(queryset=CompanyAttractionSource.objects.all(), label_field='val', empty_label="Выбрать значение...",  help_text="От куда клиент узнал о нас?")

    class Meta:
        model = Companies
        required_css_class = 'required'
        fields = ('name', 'attr_source', 'description', 'comment')


class CompanyCreatePrivateForm(CompanyCreateForm):
    name = None
    description = None

    class Meta:
        model = Companies
        required_css_class = 'required'
        fields = ('attr_source', 'comment')


class CompanyUpdateForm(CompanyCreateForm):
    description = CharField(label="Описание деятельности", required=False, help_text="Описание основных направлений деятельности", widget=TextInput(attrs={'placeholder': "Строительство, Юридические услуги", 'size': 50}))

    class Meta:
        model = Companies
        fields = ('name', 'attr_source', 'description', 'comment')


class BranchUpdateForm(ModelForm):
    name = CharField(label="Наименование отделения", required=True, help_text="Краткое наименование отделения")
    type = ModelChoiceFieldNameLabel(queryset=BranchTypes.objects.all(), label_field='val', label="Тип отделения", empty_label=None, initial=2)
    description = CharField(label="Описание отделения", required=False, widget=TextInput(attrs={'size': 40, 'maxlength': 250}))

    class Meta:
        model = Branches
        fields = ('name', 'type', 'description')


class BranchCompanyCreateForm(ModelForm):
    name = CharField(required=True, widget=HiddenInput(), initial="Основной офис")
    branch_switch = CharField(max_length=100, widget=HiddenInput, required=False)

    class Meta:
        model = Branches
        fields = ('name', 'branch_switch')


class AddressUpdateForm(ModelForm):
    city = CharField(label="Населенный пункт", required=True, widget=TextInput(attrs={'size': 25, 'id': 'input_city', 'data-kladr-type':'city', 'data-kladr-id': '7700000000000'},))
    postalcode = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    street = CharField(label="Улица", required=True,  widget=TextInput(attrs={'size': 36, 'maxlength': 250}))
    app = CharField(label="Дом, Корпус", required=True, widget=TextInput(attrs={'size': 3}))
    comment = CharField(label="Примечание к адресу", required=False, widget=forms.Textarea(attrs={'cols': 38, 'rows':2, 'maxlength': 250}))
    # exclude = ('company',)

    class Meta:
        model = Addresses
        fields = ('postalcode', 'city', 'street', 'app', 'comment')


class CompanyContactsCreateForm(ModelForm):
    show_in_card = BooleanField(widget=HiddenInput(), required=False, initial=True)

    class Meta:
        model = CompanyContacts
        fields = ('show_in_card',)


class CompanyClientOptionsForm(ModelForm):
    pay_form_choices = [('1', 'Наличная'), ('2', 'Безналичная')]

    request_tickets = BooleanField(widget=HiddenInput(), required=False, initial=True)
    request_special_sign = BooleanField(widget=HiddenInput(), required=False, initial=True)
    request_freq = IntegerField(label="Частота вывоза", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    use_client_talons_only = BooleanField(widget=HiddenInput(), required=False, initial=True)
    pay_condition = IntegerField(label="Условия оплаты", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    pay_form = ChoiceField(label="Основная Форма оплаты", choices=pay_form_choices,  widget=RadioSelect())
    pay_type = IntegerField(label="Тип оплаты", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))
    credit_limit = IntegerField(label="Кредитный лимит", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    class Meta:
        model = CompanyContacts
        fields = ('request_tickets', 'request_special_sign', 'request_freq', 'use_client_talons_only', 'pay_condition', 'pay_form', 'pay_type', 'credit_limit',)