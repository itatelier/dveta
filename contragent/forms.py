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

#
# class PersonEditForm(ModelForm):
#     family_name = CharField(label="Фамилия", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#     given_name = CharField(label="Имя", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#     middle_name = CharField(label="Отчество", required=False, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#     nick_name = CharField(label="Прозвище / Nick", required=False, widget=forms.TextInput(attrs={'size': 15, 'maxlength': 15}))
#     date_ofbirth = DateField(label="Дата рождения", required=False, widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10}))
#
#     class Meta:
#         model = Persons
#         fields = ('family_name', 'given_name', 'middle_name', 'nick_name', 'date_ofbirth')
#
#
# class PersonCompanyCreateForm(ModelForm):
#     nick_name = CharField(label="Контактное лицо", required=True, widget=forms.TextInput(attrs={'size': 25, 'maxlength': 60}), help_text="Фамилия или имя, а лучше все сразу!")
#     contact_switch = CharField(max_length=100, widget=HiddenInput, required=False)
#     # contact_exist = ChoiceField(choices=CHOICES, widget=RadioSelect())
#
#     class Meta:
#         model = Persons
#         fields = ('nick_name', 'contact_switch')
#
#
# class ContactFirmCreateForm(ModelForm):
#     role = CharField(label="Должность в компании", required=False, widget=forms.TextInput(attrs={'size': 20, 'maxlength': 60}))
#     email = EmailField(label="E-mail", required=False, widget=TextInput(attrs={'size': 40, 'maxlength': 60}))
#     comment = CharField(label="Примечание", required=False, widget=forms.TextInput(attrs={'size': 13, 'maxlength': 50}))
#     phonenumber = IntegerField(label="Номер телефона", help_text="10 цифр, в формате 9991234567", required=True, widget=forms.TextInput(attrs={'size': 7, 'maxlength': 10}))
#
#     class Meta:
#         model = Contacts
#         fields = ('role', 'email', 'comment', 'phonenumber')
#
#     # def __init__(self, *args, **kwargs):
#     #     super(ContactFirmCreateForm, self).__init__(*args, **kwargs)
#     #     if self.errors:
#     #         for f_name in self.fields:
#     #             if f_name in self.errors:
#     #                 classes = self.fields[f_name].widget.attrs.get('class', '')
#     #                 classes += ' error'
#     #                 self.fields[f_name].widget.attrs['class'] = classes
#
#
# class ContactsCreateForm(ContactFirmCreateForm):
#
#     class Meta:
#         model = Contacts
#         fields = ('role', 'email', 'comment', 'phonenumber')
#
#
#
