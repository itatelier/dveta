# -*- coding: utf8 -*

from re import sub
from django.forms import *
from models import *
from common.forms import *

import logging
log = logging.getLogger('django')


class CompanyEditForm(ModelForm):
    name = CharField(label="Наименование", required=True, help_text="Краткое наименование клента, без организационной формы")
    attr_source = ModelChoiceFieldNameLabel(queryset=CompanyAttractionSource.objects.all(), label_field='val', empty_label=None, initial=1)
    description = CharField(label="Описание компании", required=False, widget=forms.Textarea(attrs={'cols': 60, 'rows':2}))
    # www = CharField(label="WEB сайт", required=False, widget=forms.TextInput(attrs={'size': 50}))

    class Meta:
        model = Companies
        required_css_class = 'required'
        fields = ('name', 'attr_source', 'description', 'www')
        #def clean_www(self):
        #    val = self.cleaned_data['www']
        #    ret_str = sub("(http://)", '', val)
        #    log.info("field val: %s cleaned %s" % (val, ret_str))
        #    return ret_str