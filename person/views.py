
# App spcific
from models import *
from company.models import *
# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from django.views.generic.base import TemplateView
# API
from serializers import *
from rest_framework import viewsets, generics, filters


class ContactsClientsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Contacts.objects.filter(company__rel_type=2).select_related('person', 'company', 'company__status', 'company__org_type', 'company__client_options')
    serializer_class = ContactsSerializer
    filter_class = ContactsFilters
    search_fields = ('role', 'comment', 'email', 'phonenumber', 'company__name', 'person__nick_name')
    ordering_fields = ('id', 'role', 'company__name', 'company__org_type', 'company__status', 'person', 'date_add')


class PersonsContactClientsView(LoginRequiredMixin, TemplateView):
    template_name = "persons/list_contacts.html"