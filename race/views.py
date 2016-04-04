# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone
from django.shortcuts import get_object_or_404
from common.forms import *


from models import *
# from phones.models import *
from person.forms import *
from forms import *
from contragent.models import *
from rest_framework import viewsets, generics, filters
from django.http import HttpResponseRedirect
from serializers import *


class CompanyCreateFirmView(MultiFormCreate):
    template_name = 'company/company_create_firm.html'
    formconf = {
        'company': {'formclass': CompanyCreateForm},
        'branch': {'formclass': BranchCompanyCreateForm},
        'address': {'formclass': AddressUpdateForm},
        'person': {'formclass': PersonCompanyCreateForm},
        'contact': {'formclass': ContactCreateForm},
        'company_contact': {'formclass': CompanyContactForm},
    }

    def get_success_url(self, company_id):
        if company_id:
            url = reverse('company_card_client', args=[company_id])
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url