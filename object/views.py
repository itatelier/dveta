# -*- coding: utf8 -*

# App spcific
from models import *
from forms import *
from company.forms import AddressUpdateForm, AddressNoPostalForm

# API
from serializers import *
from person.serializers import *
from rest_framework import viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from common.forms import *


class ObjectsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Objects.objects.select_related('type', 'company', 'address', 'company__client_options', 'company__status', 'company__org_type', 'company__rel_type')
    # queryset = Objects.objects.select_related('type', 'company',)
    #queryset = Objects.objects.all()
    serializer_class = ObjectsSerializer
    search_fields = ('name', 'company__name', 'address__street')
    filter_class = ObjectFilters
    ordering_fields = ('type',)


class ObjectCreateView(MultiFormCreate):
    template_name = 'object/object_create.html'
    formconf = {
        'object': {'formclass': ObjectForm},
        'address': {'formclass': AddressNoPostalForm}
    }

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        aform = forms['address']
        oform = forms['object']
        if oform.is_valid() and aform.is_valid():
            company_pk = kwargs.pop('company_pk', None)
            company_object = Companies(pk=company_pk)
            address_object = aform.save()
            object_object = oform.save(commit=False)
            object_object.company = company_object
            object_object.address = address_object
            object_object.type = ObjectTypes(pk=3)
            object_object.save()
            self.success_url = '/company/%s/card' % company_pk
            return HttpResponseRedirect(self.get_success_url())
        else:
            # forms = self.get_forms()
            return self.render_to_response(self.get_context_data(forms=forms))

    def get_context_data(self, *args, **kwargs):
        context_data = super(ObjectCreateView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        context_data.update({'company': Companies.objects.get(pk=company_pk)})
        return context_data

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs.get('company_pk', None)
        return "/company/%s/card" % pk


class ClientObjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'company/company_objects.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(ClientObjectsView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        context_data['objects_and_remains'] = Objects.objects.list_bunker_remains(company_pk)
        context_data['company'] = Companies.objects.get(pk=company_pk)
        return context_data
