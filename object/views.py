# -*- coding: utf8 -*

# App spcific
from models import *
from forms import *
from company.forms import AddressUpdateForm

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
    serializer_class = ObjectsSerializer
    search_fields = ('name', 'company__name', 'address__street')
    filter_class = ObjectFilters
    ordering_fields = ('type',)


class ObjectCreateView(MultiFormCreate):
    template_name = 'object/object_create.html'
    formconf = {
        'object': {'formclass': ObjectForm},
        'address': {'formclass': AddressUpdateForm}
    }

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        aform = forms['address']
        bform = forms['branch']
        if bform.is_valid() and aform.is_valid():
            company_pk = kwargs.pop('company_pk', None)
            company_object = Companies(pk=company_pk)
            address_object = aform.save()
            branch_object = bform.save(commit=False)
            branch_object.company = company_object
            branch_object.address = address_object
            branch_object.save()
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