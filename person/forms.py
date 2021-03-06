# -*- coding: utf8 -*

from django.forms import *
from models import *
from company.models import *
from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_phone(value):
    if value % 2 != 0:
        raise ValidationError('%s is not an even number' % value)


class PersonUpdateForm(ModelForm):
    family_name = CharField(label="Фамилия", required=True, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))
    given_name = CharField(label="Имя", required=True, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))
    middle_name = CharField(label="Отчество", required=False, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))
    nick_name = CharField(label="Прозвище / Nick", required=False, widget=TextInput(attrs={'size': 15, 'maxlength': 15}))
    date_ofbirth = DateField(label="Дата рождения", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10}))

    class Meta:
        model = Persons
        fields = ('family_name', 'given_name', 'middle_name', 'nick_name', 'date_ofbirth')


class PersonEmployeeCreateForm(ModelForm):
    family_name = CharField(label="Фамилия", required=True, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))
    given_name = CharField(label="Имя", required=True, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))
    nick_name = CharField(label="Прозвище / Nick", required=False, widget=TextInput(attrs={'size': 15, 'maxlength': 15}))

    class Meta:
        model = Persons
        fields = ('family_name', 'given_name', 'nick_name')


class PersonCompanyCreateForm(ModelForm):
    nick_name = CharField(label="Контактное лицо", required=True, widget=TextInput(attrs={'size': 25, 'maxlength': 60}), help_text="Фамилия или имя, а лучше все сразу!")
    contact_switch = CharField(max_length=100, widget=HiddenInput, required=False)
    # contact_exist = ChoiceField(choices=CHOICES, widget=RadioSelect())

    class Meta:
        model = Persons
        fields = ('nick_name', 'contact_switch')

    def __init__(self, *args, **kwargs):
        super(PersonCompanyCreateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['nick_name'].widget.attrs['readonly'] = True

    def clean_nick_name(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.nick_name
        else:
            return self.cleaned_data['nick_name']


class CompanyContactForm(ModelForm):
    role = CharField(label="Должность в компании", required=False, widget=TextInput(attrs={'size': 20, 'maxlength': 60}))
    email = EmailField(label="E-mail", required=False, widget=TextInput(attrs={'size': 40, 'maxlength': 60}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 13, 'maxlength': 50}))
    show_in_card = BooleanField(widget=HiddenInput(), required=False, initial=True)

    class Meta:
        model = CompanyContacts
        fields = ('role', 'email', 'comment', 'show_in_card')


class ContactCreateForm(ModelForm):
    phonenumber = CharField(
        label="Номер телефона",
        help_text="10 цифр, в формате 9991234567",
        validators=[
            RegexValidator(
                regex='^[0-9]{10}$',
                message='Номер должен состоять из 10 цифр!',
                code='invalid_input'
            )],
        required=True,
        widget=TextInput(attrs={'size': 7, 'maxlength': 10}))

    class Meta:
        model = Contacts
        fields = ('phonenumber',)

    def clean(self):
        cleaned_data = super(ContactCreateForm, self).clean()
        phonenumber = cleaned_data.get("phonenumber")
        phone_object = None
        try:
            phone_object = Contacts.objects.select_related('person').get(phonenumber=phonenumber)
        except Contacts.DoesNotExist:
            x = None

        if phone_object:
            msg = u"Номер телефона уже присвоен персоне %s %s [%s] (id# %s)" % (phone_object.person.family_name, phone_object.person.given_name, phone_object.person.nick_name, phone_object.person.pk)
            self.add_error('phonenumber', msg)


class EmployeeEditForm(ModelForm):
    type = ModelChoiceFieldNameLabel(queryset=EmployeeTypes.objects.all(), label_field='val', label="Тип сотрудника", empty_label=None, initial=2)
    role = ModelChoiceFieldNameLabel(queryset=EmployeeRoles.objects.all(), label_field='val', label="Роль сотрудника", empty_label=None, initial=2)
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))

    class Meta:
        model = Employies
        fields = ('type', 'role', 'comment')


class EmployeeUpdateSalaryForm(ModelForm):
    mobile_compensation_choices = [(False, 'Не начисляется'), (True, 'Начисляется')]
    basehouse_rent_choices = [(False, 'Не начисляется'), (True, 'Удерживать из ЗП')]

    acr_ndfl_sum = DecimalField(label="Сумма налога НДФЛ для удержания (руб.)", required=True, decimal_places=2, widget=TextInput(attrs={'size': 3, 'style': 'min-width:6rem;'}))
    acr_mobile_compensation = ChoiceField(label="Компенсация за мобильную связь", choices=mobile_compensation_choices, initial=False, widget=widgets.RadioSelect())
    acr_basehouse_rent = ChoiceField(label="Вычет за проживание на базе", choices=basehouse_rent_choices, initial=False, widget=widgets.RadioSelect())

    class Meta:
        model = Employies
        fields = ('acr_ndfl_sum', 'acr_mobile_compensation', 'acr_basehouse_rent')




