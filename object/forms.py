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
    name = CharField(label="Наименование", help_text="Наименование объекта", required=True, widget=TextInput(attrs={'size': 40, 'maxlength': 200}))
    salary_spec_price = DecimalField(label="Спец тариф за ходку для водителя", help_text="0 - не считать", required=False, initial=0, widget=TextInput(attrs={'size': 4, 'maxlength': 4}))

    class Meta:
        model = Objects
        fields = ('name',)
