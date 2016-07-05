# -*- coding: utf8 -*

from django.forms import *
from django.db.models import Q
from models import *
from company.models import *
from person.models import *
from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from refuels.models import *


def validate_phone(value):
    if value % 2 != 0:
        raise ValidationError('%s is not an even number' % value)


class EmployeeChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.person.family_name, obj.person.given_name)


class CarCreateForm(ModelForm):
    reg_num = CharField(label="Гос. Номер", help_text="Номер государственной регистрации в формате A123BC777", required=True, widget=TextInput(attrs={'size': 10, 'maxlength': 10}))
    nick_name = CharField(label="Ник", help_text="Краткое наименование авто", required=True, widget=TextInput(attrs={'size': 10, 'maxlength': 10}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 60, 'maxlength': 60}))
    model = ModelChoiceField(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
    fuel_type = ModelChoiceFieldNameLabel(queryset=CarFuelTypes.objects.all(), label_field='val', label="Тип топлива", empty_label=None)
    mechanic = EmployeeChoiceField(queryset=Employies.mechanics.all(), label="Механик", empty_label=None)
    unit_group = ModelChoiceField(queryset=UnitGroups.objects.all(), label="Группа", empty_label=None)

    class Meta:
        model = Cars
        fields = ('reg_num', 'nick_name', 'model', 'fuel_type', 'mechanic', 'unit_group', 'comment')


class CarCreateWithoutComment(CarCreateForm):
    comment = CharField(label="Примечание", required=False, widget=HiddenInput())


class CarDriverUpdateForm(ModelForm):
    driver = EmployeeChoiceField(queryset=Employies.drivers.select_related('person').filter(status__pk=1), required=False, label="Водитель", help_text="Выбор из списка работающих водителей", empty_label="Не назначен")

    class Meta:
        model = Cars
        fields = ('driver', )


class CarFuelCardUpdateForm(ModelForm):
    fuel_card = ModelChoiceField(queryset=FuelCards.objects.exclude(assigned_to_car__isnull=False), required=False, label="Новая топливная карта", help_text="Выбор топливной карты из списка доступных", empty_label=None)

    class Meta:
        model = Cars
        fields = ('fuel_card', )


class CarDocsForm(ModelForm):
    owner = ModelChoiceField(queryset=CarOwners.objects.all(), label="Владелец авто", help_text="владелец авто по регистрационным документам", empty_label=None)
    ins_number = CharField(label="Номер полиса", required=False, widget=TextInput(attrs={'size': 10, 'maxlength': 20}))
    ins_date_register = DateField(label="Дата регистрации", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 7, 'maxlength': 10, 'placeholder' :"дд-мм-гггг"}))
    ins_date_end = DateField(label="Дата окончания", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 7, 'maxlength': 10, 'placeholder' :"дд-мм-гггг", 'class': 'icon', 'icon': ''}))
    ins_price = DecimalField(label="Стоимость",max_digits=10, decimal_places=0, required=False, widget=TextInput(attrs={'size': 6, 'maxlength': 6}))
    ins_comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 20, 'maxlength': 200}))
    to_number = CharField(label="Номер документа", required=False, widget=TextInput(attrs={'size': 10, 'maxlength': 10}))
    to_date_end = DateField(label="Дата окончания", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10, 'placeholder' :"дд-мм-гггг"}))
    rent_date_end = DateField(label="Дата окончания", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10, 'placeholder' :"дд-мм-гггг"}))
    fuel_card = ModelChoiceField(queryset=FuelCards.objects.all(), label="Топливная карта", empty_label="-- не привязана --", required=False)

    class Meta:
        model = CarDocs
        fields = ('owner', 'ins_number', 'ins_date_register', 'ins_date_end', 'ins_price', 'ins_comment', 'to_number', 'to_date_end', 'rent_date_end', 'fuel_card')

