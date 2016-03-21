# -*- coding: utf8 -*

from re import sub
from django.forms import *
from django.forms.widgets import ChoiceFieldRenderer, RendererMixin, RadioFieldRenderer, RadioChoiceInput
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html, html_safe

from models import *
from common.forms import *
from common.formfields import *


import logging
log = logging.getLogger('django')


class CompanyCreateForm(ModelForm):
    name = CharField(label="Наименование", required=True, help_text="Краткое наименование клента, простое, как \"Утюг\"")
    description = CharField(label="Род деятельности", required=False, help_text="Описание деятельности компании", widget=TextInput(attrs={'placeholder': "Строительство, Юридические услуги", 'size': 50}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 40}))
    attr_source = ModelChoiceFieldNameLabel(label="Источник привлечения", queryset=CompanyAttractionSource.objects.all(), label_field='val', empty_label="Выбрать значение...",  help_text="От куда клиент узнал о нас?")

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
    comment = CharField(label="Примечание к адресу", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows':1, 'maxlength': 250}))
    lat = FloatField(required=True, widget=HiddenInput())
    lng = FloatField(required=True, widget=HiddenInput())
    # exclude = ('company',)

    class Meta:
        model = Addresses
        fields = ('postalcode', 'city', 'street', 'app', 'comment', 'lat', 'lng')


class AddressNoPostalForm(AddressUpdateForm):
    postalcode = None

    def __init__(self, *args, **kwargs):
        super(AddressNoPostalForm, self).__init__(*args, **kwargs)
        del self.fields['postalcode']


class CompanyContactsCreateForm(ModelForm):
    show_in_card = BooleanField(widget=HiddenInput(), required=False, initial=True)

    class Meta:
        model = CompanyContacts
        fields = ('show_in_card',)


class CompanyClientOptionsForm(ModelForm):
    pay_form_choices = [('1', 'Наличная'), ('2', 'Безналичная')]
    pay_type_choices = [('1', 'Предоплата'), ('2', 'По факту')]
    request_freq_choices = [('1', 'Обычный клиент'), ('2', 'Постоянный клиент')]
    pay_condition_choices = [('1', 'По постановке'), ('2', 'По вывозу')]

    request_tickets = BooleanField(label="Предоставлять талоны с полигонов", required=False)
    request_special_sign = BooleanField(label="Делать отметки на объектах", required=False, )
    request_freq = ChoiceField(label="Частота вывоза", choices=request_freq_choices, required=False, widget=RadioSelect(renderer=RadioRendererSimple))
    use_client_talons_only = BooleanField(widget=HiddenInput(), required=False, initial=True)
    pay_condition = ChoiceField(label="Условия оплаты", choices=pay_condition_choices, required=False, widget=RadioSelect(renderer=RadioRendererSimple))
    pay_form = ChoiceField(label="Основная Форма оплаты", choices=pay_form_choices,  widget=RadioSelect(renderer=RadioRendererSimple))
    pay_type = ChoiceField(label="Тип оплаты", choices=pay_type_choices,  widget=RadioSelect(renderer=RadioRendererSimple))
    credit_limit = IntegerField(label="Кредитный лимит", required=False, widget=TextInput(attrs={'size': 5, 'maxlength': 6}))

    class Meta:
        model = ClientOptions
        fields = ('request_tickets', 'request_special_sign', 'request_freq', 'use_client_talons_only', 'pay_condition', 'pay_form', 'pay_type', 'credit_limit',)