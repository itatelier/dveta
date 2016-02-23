# -*- coding: utf8 -*

from django.forms import *
from models import *
from company.models import *
from person.models import *
from object.models import Objects
from common.forms import *
from common.formfields import *
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import logging
log = logging.getLogger('django')


class ObjectForm(ModelForm):
    name = CharField(label="Наименование", help_text="Наименование объекта", required=True, widget=forms.TextInput(attrs={'size': 30, 'maxlength': 10}))

    class Meta:
        model = Objects
        fields = ('name',)


#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     name = models.CharField(max_length=200L, null=False, blank=False)
#     type = models.ForeignKey('ObjectTypes', null=False, blank=False, editable=True)
#     company = models.ForeignKey('company.Companies', null=False, blank=False, editable=True)
#     address = models.ForeignKey('company.Addresses', null=False, blank=False, editable=True)
#     date_add = models.DateTimeField(auto_now_add=True)
#     date_update = models.DateTimeField(auto_now=True)
#
# class BunkerFlowForm(ModelForm):
#     object_out = ModelChoiceFieldNoOpt(
#         queryset=Objects.objects.all(),
#         label="Исходный объект",
#         help_text="объект, с которого переходит бункер",
#         label_field="name",
#         required=True,
#         widget=Select(attrs={
#             'size': 10,
#             'class': "select2_powered"
#         }))
#     object_in = ModelChoiceFieldNoOpt(
#         queryset=Objects.objects.all(),
#         label="Объект назначения",
#         help_text="объект на который переходит бункер",
#         label_field="name",
#         required=True,
#         widget=Select(attrs={
#             'size': 10,
#             'class': "select2_powered",
#         }))
#     qty = DecimalField(label="Количество", max_digits=10, decimal_places=0, required=False, widget=forms.TextInput(attrs={'size': 6, 'maxlength': 6}))
#     bunker_type = ModelChoiceFieldNameLabel(queryset=BunkerTypes.objects.all(), label_field="val", label="Тип бункера", empty_label=None)
#     operation_type = ModelChoiceFieldNameLabel(queryset=BunkerOperationTypes.objects.all(), label_field="val",label="Операция", empty_label=None)
#
#     class Meta:
#         model = BunkerFlow
#         fields = ('object_in', 'object_out', 'qty', 'bunker_type', 'operation_type')
#
#
#
#
# def validate_phone(value):
#     if value % 2 != 0:
#         raise ValidationError('%s is not an even number' % value)
#
#
# class EmployeeChoiceField(ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s %s" % (obj.person.family_name, obj.person.given_name)
#
#
# class CarCreateForm(ModelForm):
#     reg_num = CharField(label="Гос. Номер", help_text="Номер государственной регистрации в формате A123BC777", required=True, widget=forms.TextInput(attrs={'size': 10, 'maxlength': 10}))
#     nick_name = CharField(label="Ник", help_text="Краткое наименование авто", required=True, widget=forms.TextInput(attrs={'size': 10, 'maxlength': 10}))
#     comment = CharField(label="Примечание", required=False, widget=forms.TextInput(attrs={'size': 60, 'maxlength': 60}))
#     model = ModelChoiceField(queryset=CarModels.objects.all(), label="Модель авто", empty_label=None)
#     fuel_type = ModelChoiceFieldNameLabel(queryset=CarFuelTypes.objects.all(), label_field='val', label="Тип топлива", empty_label=None)
#     mechanic = EmployeeChoiceField(queryset=Employies.mechanics.all(), label="Механик", empty_label=None)
#     unit_group = ModelChoiceField(queryset=UnitGroups.objects.all(), label="Группа", empty_label=None)
#
#     class Meta:
#         model = Cars
#         fields = ('reg_num', 'nick_name', 'model', 'fuel_type', 'mechanic', 'unit_group', 'comment')
#
#
# class CarDriverUpdateForm(ModelForm):
#     driver = EmployeeChoiceField(queryset=Employies.drivers.select_related('person').filter(status__pk=1), required=False, label="Водитель", help_text="Выбор из списка работающих водителей", empty_label="Не назначен")
#
#     class Meta:
#         model = Cars
#         fields = ('driver', )
#
#
# class CarDocsForm(ModelForm):
#     owner = ModelChoiceField(queryset=CarOwners.objects.all(), label="Владелец авто", help_text="владелец авто по регистрационным документам", empty_label=None)
#     ins_number = CharField(label="Номер полиса", required=False, widget=forms.TextInput(attrs={'size': 10, 'maxlength': 20}))
#     ins_date_register = DateField(label="Дата регистрации", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 7, 'maxlength': 10, 'placeholder' :"дд-мм-гггг"}))
#     ins_date_end = DateField(label="Дата окончания", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 7, 'maxlength': 10, 'placeholder' :"дд-мм-гггг", 'class': 'icon', 'icon': ''}))
#     ins_price = DecimalField(label="Стоимость",max_digits=10, decimal_places=0, required=False, widget=forms.TextInput(attrs={'size': 6, 'maxlength': 6}))
#     ins_comment = CharField(label="Примечание", required=False, widget=forms.TextInput(attrs={'size': 20, 'maxlength': 200}))
#     to_number = CharField(label="Номер документа", required=False, widget=forms.TextInput(attrs={'size': 10, 'maxlength': 10}))
#     to_date_end = DateField(label="Дата окончания", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10, 'placeholder' :"дд-мм-гггг"}))
#     rent_date_end = DateField(label="Дата окончания", required=False, input_formats=('%d-%m-%Y',), widget=RuDateWidget(attrs={'size': 10, 'maxlength': 10, 'placeholder' :"дд-мм-гггг"}))
#
#     class Meta:
#         model = CarDocs
#         fields = ('owner', 'ins_number', 'ins_date_register', 'ins_date_end', 'ins_price', 'ins_comment', 'to_number', 'to_date_end', 'rent_date_end')
#
