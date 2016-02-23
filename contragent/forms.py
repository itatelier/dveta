# -*- coding: utf8 -*

from django.forms import *
from models import *
from company.models import *
from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList


class ContragentUlEditForm(ModelForm):
    name = CharField(label="Наименование", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    inn = CharField(label="ИНН", required=True, min_length=10, widget=forms.TextInput(attrs={'size': 10, 'maxlength': 10}))
    kpp = CharField(label="КПП", required=True, min_length=9,  widget=forms.TextInput(attrs={'size': 9, 'maxlength': 9}))
    ogrn = CharField(label="ОГРН", required=False, min_length=13,  widget=forms.TextInput(attrs={'size': 13, 'maxlength': 13}))
    uraddress = CharField(label="Юр. Адрес", required=True, widget=forms.TextInput(attrs={'size': 80}))
    comment = CharField(label="Комментарий", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 2}))

    class Meta:
        model = Contragents
        fields = ('name', 'inn', 'kpp', 'ogrn', 'uraddress', 'comment')


class ContragentIpEditForm(ModelForm):
    name = CharField(label="Ф.И.О.", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    inn = CharField(label="ИНН", required=True, min_length=12, widget=forms.TextInput(attrs={'size': 12, 'maxlength': 12}))
    uraddress = CharField(label="Адрес прописки", required=True, widget=forms.TextInput(attrs={'size': 60}))
    comment = CharField(label="Комментарий", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 2}))

    class Meta:
        model = Contragents
        fields = ('name', 'inn', 'uraddress', 'comment')


class ContragentFlEditForm(ModelForm):
    name = CharField(label="Ф.И.О.", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    inn = CharField(label="ИНН", required=False, min_length=12, widget=forms.TextInput(attrs={'size': 12, 'maxlength': 12}))
    uraddress = CharField(label="Адрес прописки", required=False, widget=forms.TextInput(attrs={'size': 60}))
    comment = CharField(label="Комментарий", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows': 2}))

    class Meta:
        model = Contragents
        fields = ('name', 'inn', 'uraddress', 'comment')
