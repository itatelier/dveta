# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404


# API
from serializers import *
from company.serializers import *
from rest_framework import viewsets, generics, filters

import logging
log = logging.getLogger('django')


class GetContactViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = CompanyContacts.objects.select_related('company', 'contact', 'contact__person')
    serializer_class = CompanyContactsSerializerShort
    filter_class = CompanyContactsFilters


class CreateCompanyContactJsonView(JsonViewMix):
    param_names = ['company_id', 'contact_id']
    login_required = True

    def prepare(self, *args, **kwargs):
        find_filters = {
            'company_id': self.values['company_id'],
            'contact_id': self.values['contact_id']
        }

        company_contact_exist_object = CompanyContacts.objects.filter(**find_filters)
        if company_contact_exist_object:
            self.errors.append("Контакт уже связан с компанией!")
        else:
            company_contact_object = CompanyContacts.objects.create(
                company_id=self.values['company_id'],
                contact_id=self.values['contact_id']
            )
            company_contact_object.save()
            self.values['Success'] = 'true'
            log.info("New object saved")
        return