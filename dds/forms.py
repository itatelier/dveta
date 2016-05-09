# -*- coding: utf8 -*

from re import sub
from django.forms import *
from django.forms.widgets import ChoiceFieldRenderer, RendererMixin, RadioFieldRenderer, RadioChoiceInput
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.html import conditional_escape, format_html, html_safe

from models import *
from common.forms import *
from common.formfields import *


class AdminItemForm(ModelForm):
    direction_choices = [('0', 'Статья расхода'), ('1', 'Статья прихода')]
    direction_type = BooleanField(initial=0, label="Тип направления", widget=RadioSelect( choices=direction_choices))
    item_group = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), label_field='name', label="Группа статей", empty_label=None, initial=1)
    name = CharField(label="Наименование статьи учета", required=True, help_text="Краткое наименование статьи учета")

    class Meta:
        model = DdsItems
        fields = ('item_group', 'name', 'direction_type')


# class IncomeOperationForm(ModelForm):
#     item_group = ModelChoiceFieldNameLabel(queryset=DdsItemGroups.objects.all(), label_field='val', label="Тип отделения", empty_label=None, initial=2)
#
#
#     # name = CharField(label="Наименование отделения", required=True, help_text="Краткое наименование отделения")
#     # type = ModelChoiceFieldNameLabel(queryset=BranchTypes.objects.all(), label_field='val', label="Тип отделения", empty_label=None, initial=2)
#     # description = CharField(label="Описание отделения", required=False, widget=TextInput(attrs={'size': 40, 'maxlength': 250}))
#
#     class Meta:
#         model = DdsFlow
#         fields = ('name', 'type', 'description')