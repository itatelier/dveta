
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

# class ContactsClientsViewSet(viewsets.ModelViewSet):
#     filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     queryset = Contacts.objects.filter(company__rel_type=2).select_related('person', 'company', 'company__status', 'company__org_type', 'company__client_options')
#     serializer_class = ContactsSerializer
#     filter_class = ContactsFilters
#     search_fields = ('role', 'comment', 'email', 'phonenumber', 'company__name', 'person__nick_name')
#     ordering_fields = ('id', 'role', 'company__name', 'company__org_type', 'company__status', 'person', 'date_add')


class PersonsContactClientsView(LoginRequiredMixin, TemplateView):
    template_name = "persons/list_contacts.html"


class GetContactViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    queryset = CompanyContacts.objects.select_related('company', 'contact', 'contact__person')
    serializer_class = CompanyContactsSerializer
    filter_class = CompanyContactsFilters


class CreateCompanyContactJsonView(JsonViewMix):
    param_names = ['company_id', 'contact_id']
    login_required = True

    def prepare(self, *args, **kwargs):
        company_contact_object = CompanyContacts.objects.create(
            company_id=self.values['company_id'],
            contact_id=self.values['contact_id']
        )
        company_contact_object.save()
        self.values['Success'] = 'true'
        log.info("New object saved")
        return