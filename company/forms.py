# -*- coding: utf8 -*

from re import sub
from django.forms import *
from models import *
from common.forms import *

import logging
log = logging.getLogger('django')


class CompanyCreateForm(ModelForm):
    name = CharField(label="Наименование", required=True, help_text="Краткое наименование клента, простое, как \"Утюг\"")
    description = CharField(label="Род деятельности", required=True, help_text="Перечень основных видов деятельности", widget=TextInput(attrs={'placeholder': "Строительство, Юридические услуги", 'size': 50}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 40}))
    attr_source = ModelChoiceFieldNameLabel(queryset=CompanyAttractionSource.objects.all(), label_field='val', empty_label=None, initial=1, help_text="От куда клиент узнал о нас?")
    # org_type = ModelChoiceField(queryset=CompanyOrgTypes.objects.all(), widget=HiddenInput())
    # rel_type = ModelChoiceField(queryset=CompanyRelTypes.objects.all(), widget=HiddenInput())
    # status = ModelChoiceField(queryset=CompanyStatus.objects.all())

    class Meta:
        model = Companies
        required_css_class = 'required'
        fields = ('name', 'attr_source', 'description', 'comment')


class BranchEditForm(ModelForm):
    name = CharField(label="Наименование отделения", required=True, help_text="Краткое наименование отделения")
    type = ModelChoiceFieldNameLabel(queryset=BranchTypes.objects.all().exclude(pk=1), label_field='val', label="Тип отделения", empty_label=None, initial=1)
    description = CharField(label="Описание отделения", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows':2}))

    class Meta:
        model = Branches
        fields = ('name', 'type', 'description')


class BranchCompanyCreateForm(ModelForm):
    name = CharField(required=True, widget=HiddenInput(), initial="Основной офис")
    # company_main = IntegerField(required=True, widget=HiddenInput())

    class Meta:
        model = Branches
        fields = ('name',)


class AddressEditForm(ModelForm):
    city = CharField(label="Населенный пункт", required=True)
    postalcode = IntegerField(label="Почтовый код", required=False, widget=TextInput(attrs={'size': 5}))
    street = CharField(label="Улица", required=True)
    app = CharField(label="Дом", required=True, widget=TextInput(attrs={'size': 2}))
    app_extra = CharField(label="Корпус / Строение", required=False, widget=TextInput(attrs={'size': 2}))
    comment = CharField(label="Примечание к адресу", required=False)
    # exclude = ('company',)

    class Meta:
        model = Addresses
        fields = ('postalcode', 'city', 'street', 'app', 'app_extra', 'comment')