# -*- coding: utf8 -*

from django.forms import *
from models import *
from company.models import *
from common.forms import *


class PersonEditForm(ModelForm):
    family_name = CharField(label="Фамилия", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    given_name = CharField(label="Имя", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    middle_name = CharField(label="Отчество", required=False, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    nick_name = CharField(label="Прозвище / Nick", required=False, widget=forms.TextInput(attrs={'size': 15, 'maxlength': 15}))
    date_ofbirth = DateField(label="Дата рождения", required=False, widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10}))

    class Meta:
        model = Persons
        fields = ('family_name', 'given_name', 'middle_name', 'nick_name', 'date_ofbirth')


class PersonCompanyCreateForm(ModelForm):
    nick_name = CharField(label="Контактное лицо", required=True, widget=forms.TextInput(attrs={'size': 15, 'maxlength': 15}), help_text="Фамилия или имя, а лучше все сразу!")

    class Meta:
        model = Persons
        fields = ('nick_name',)


class ContactFirmCreateForm(ModelForm):
    role = CharField(label="Должность в компании", required=False, widget=forms.TextInput(attrs={'size': 20, 'maxlength': 60}))
    email = CharField(label="email", required=False, widget=forms.TextInput(attrs={'size': 40, 'maxlength': 60}))
    comment = CharField(label="Примечание", required=False, widget=forms.TextInput(attrs={'size': 9, 'maxlength': 50}))
    phonenumber = IntegerField(label="Номер телефона", required=True, widget=forms.TextInput(attrs={'size': 7, 'maxlength': 10}))

    class Meta:
        model = Contacts
        fields = ('role', 'email', 'comment', 'phonenumber')