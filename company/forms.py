# -*- coding: utf8 -*

from re import sub
from django.forms import *
from models import *
from common.forms import *

import logging
log = logging.getLogger('django')


class CompanyEditForm(ModelForm):
    name = CharField(label="Наименование", required=True, help_text="Краткое наименование клента, без организационной формы")
    org_type = ModelChoiceFieldNameLabel(queryset=CompanyOrgTypes.objects.all(), label_field='val', empty_label=None, initial=3)
    description = CharField(label="Описание компании", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows':2}))
    www = CharField(label="WEB сайт", required=False, widget=forms.TextInput(attrs={'size': 50}))

    class Meta:
        model = Companies
        required_css_class = 'required'
        fields = ('org_type', 'name', 'description', 'www')
        #def clean_www(self):
        #    val = self.cleaned_data['www']
        #    ret_str = sub("(http://)", '', val)
        #    log.info("field val: %s cleaned %s" % (val, ret_str))
        #    return ret_str