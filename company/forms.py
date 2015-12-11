# -*- coding: utf8 -*

from re import sub
from django.forms import *
from models import *
from common.forms import *

import logging
log = logging.getLogger('django')


class CompanyEditForm(ModelForm):
    name = CharField(label="Наименование", required=True, help_text="Краткое наименование клента, простое, как \"Утюг\"")
    description = CharField(label="Род деятельности", required=True, widget=TextInput(attrs={'placeholder': "Строительство, Юридические услуги", 'size': 50}))
    # www = CharField(label="WEB сайт", required=False, widget=forms.TextInput(attrs={'size': 50}))
    comment = CharField(label="Примечание", required=False, widget=TextInput(attrs={'size': 40}))
    attr_source = ModelChoiceFieldNameLabel(queryset=CompanyAttractionSource.objects.all(), label_field='val', empty_label=None, initial=1)
    org_type = ModelChoiceField(queryset=CompanyOrgTypes.objects.all(), widget=HiddenInput())
    rel_type = ModelChoiceField(queryset=CompanyRelTypes.objects.all(), widget=HiddenInput())
    status = ModelChoiceField(queryset=CompanyStatus.objects.all())

    class Meta:
        model = Companies
        required_css_class = 'required'
        # fields = ('name', 'description', 'comment',)
        fields = ('name', 'attr_source', 'description', 'comment', 'org_type', 'rel_type', 'status')
        # widgets = {
        #     'org_type': HiddenInput(),
        #     'rel_type': HiddenInput()
        # }
        #def clean_www(self):
        #    val = self.cleaned_data['www']
        #    ret_str = sub("(http://)", '', val)
        #    log.info("field val: %s cleaned %s" % (val, ret_str))
        #    return ret_str

