# -*- coding: utf8 -*

from django.forms import *
from models import *
from company.models import *
from person.models import *
from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_phone(value):
    if value % 2 != 0:
        raise ValidationError('%s is not an even number' % value)


class EmployeeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.person.family_name, obj.person.given_name)


class CarCreateForm(ModelForm):
    reg_num = CharField(label="Гос. Номер", help_text="Номер государственной регистрации в формате A123BC777", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    nick_name = CharField(label="Ник", help_text="Краткое наименование авто", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
    model = ModelChoiceField(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
    fuel_type = ModelChoiceFieldNameLabel(queryset=CarFuelTypes.objects.all(), label_field='val', label="Тип топлива", empty_label=None)
    mechanic = EmployeeChoiceField(queryset=Employies.mechanics.all(), label="Механик", empty_label=None)
    unit_group = ModelChoiceField(queryset=UnitGroups.objects.all(), label="Группа", empty_label=None)

    class Meta:
        model = Cars
        fields = ('reg_num', 'nick_name', 'model', 'fuel_type', 'mechanic', 'unit_group')
#
#
# class PersonEmployeeCreateForm(ModelForm):
#     family_name = CharField(label="Фамилия", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#     given_name = CharField(label="Имя", required=True, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#     nick_name = CharField(label="Прозвище / Nick", required=False, widget=forms.TextInput(attrs={'size': 15, 'maxlength': 15}))
#
#     class Meta:
#         model = Persons
#         fields = ('family_name', 'given_name', 'nick_name')
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
#     def __init__(self, *args, **kwargs):
#         super(PersonCompanyCreateForm, self).__init__(*args, **kwargs)
#         instance = getattr(self, 'instance', None)
#         if instance and instance.pk:
#             self.fields['nick_name'].widget.attrs['readonly'] = True
#
#     def clean_nick_name(self):
#         instance = getattr(self, 'instance', None)
#         if instance and instance.pk:
#             return instance.nick_name
#         else:
#             return self.cleaned_data['nick_name']
#
#
# class CompanyContactForm(ModelForm):
#     role = CharField(label="Должность в компании", required=False, widget=forms.TextInput(attrs={'size': 20, 'maxlength': 60}))
#     email = EmailField(label="E-mail", required=False, widget=TextInput(attrs={'size': 40, 'maxlength': 60}))
#     comment = CharField(label="Примечание", required=False, widget=forms.TextInput(attrs={'size': 13, 'maxlength': 50}))
#     show_in_card = BooleanField(widget=HiddenInput(), required=False, initial=True)
#
#     class Meta:
#         model = CompanyContacts
#         fields = ('role', 'email', 'comment', 'show_in_card')
#
#
# class ContactCreateForm(ModelForm):
#     phonenumber = CharField(
#         label="Номер телефона",
#         help_text="10 цифр, в формате 9991234567",
#         validators=[
#             RegexValidator(
#                 regex='^[0-9]{10}$',
#                 message='Номер должен состоять из 10 цифр!',
#                 code='invalid_input'
#             )],
#         required=True,
#         widget=forms.TextInput(attrs={'size': 7, 'maxlength': 10}))
#
#     class Meta:
#         model = Contacts
#         fields = ('phonenumber',)
#
#
# class EmployeeEditForm(ModelForm):
#     type = ModelChoiceFieldNameLabel(queryset=EmployeeTypes.objects.all(), label_field='val', label="Тип сотрудника", empty_label=None, initial=2)
#     role = ModelChoiceFieldNameLabel(queryset=EmployeeRoles.objects.all(), label_field='val', label="Роль сотрудника", empty_label=None, initial=2)
#     comment = CharField(label="Примечание", required=False, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#
#     class Meta:
#         model = Employies
#         fields = ('type', 'role', 'comment')





