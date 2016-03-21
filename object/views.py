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
    serializer_class = ObjectsSerializer
    search_fields = ('name', 'company__name', 'address__street')
    filter_class = ObjectFilters
    ordering_fields = ('type',)


class ObjectsListingViewSet(ObjectsViewSet):
    queryset = Objects.objects.filter(type__in=(1, 3)).select_related('type', 'company', 'address', 'company__client_options', 'company__status', 'company__org_type', 'company__rel_type')


class ClientObjectsView(LoginRequiredMixin, TemplateView):
    template_name = 'company/company_objects.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(ClientObjectsView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        context_data['objects_and_remains'] = Objects.objects.list_bunker_remains(company_pk)
        context_data['company'] = Companies.objects.get(pk=company_pk)
        return context_data


class ObjectListView(LoginRequiredMixin, TemplateView):
    template_name = "object/list_objects.html"


class ObjectCardView(LoginRequiredMixin, DetailView):
    template_name = "object/object_card.html"
    model = Objects
    queryset = Objects.objects.select_related('type', 'company', 'address', 'company__client_options', 'company__status', 'company__org_type', 'company__rel_type')

    def get_context_data(self, *args, **kwargs):
        object_pk = self.kwargs.get('pk', None)
        log.info("--- Card object: %s" % object_pk)
        context_data = super(ObjectCardView, self).get_context_data(*args, **kwargs)
        context_data['bunkers_onboard'] = self.object.bunker_remain.all()
        context_data['object_contacts'] = ObjectContacts.objects.filter(object=object_pk)
        return context_data


class ObjectCreateView(MultiFormCreate):
    template_name = 'object/object_create_update.html'
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
            # Сoздаем объекты "контакты на объекте"
            checked_contacts = request.POST.getlist('company_contact_id')
            if len(checked_contacts) > 0:
                for contact_id in checked_contacts:
                    company_contact_object = CompanyContacts(pk=contact_id)
                    object_contact, created = ObjectContacts.objects.update_or_create(
                                object=object_object,
                                company_contact=company_contact_object,
                    )
                    object_contact.save()
            self.success_url = '/company/%s/card' % company_pk
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(forms=forms))

    def get_context_data(self, *args, **kwargs):
        context_data = super(ObjectCreateView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        context_data.update({
            'company': Companies.objects.get(pk=company_pk),
            'contacts': CompanyContacts.objects.select_related('contact').filter(company=company_pk)
        })
        return context_data

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs.get('company_pk', None)
        return "/company/%s/card" % pk


class ObjectUpdateView(MultiFormEdit):
    template_name = "object/object_create_update.html"
    formconf = {
        'object': {'formclass': ObjectForm},
        'address': {'formclass': AddressNoPostalForm}
    }

    def get_context_data(self, *args, **kwargs):
        context_data = super(ObjectUpdateView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        object_pk = self.kwargs.get('pk', None)
        context_data.update({
            'company': Companies.objects.get(pk=company_pk),
            'object_pk': object_pk,
            'company_contacts': CompanyContacts.objects.select_related('company').filter(company=company_pk),
            'object_contacts': ObjectContacts.objects.select_related('company_contact').filter(object=object_pk)
        })
        return context_data

    def update_formconf(self, formconf, *args, **kwargs):
        object_pk = kwargs.pop('pk', None)
        info_object = Objects.objects.get(pk=object_pk)
        formconf['object']['instance'] = info_object
        formconf['address']['instance'] = info_object.address
        return formconf

    def get_success_url(self, *args, **kwargs):
        return "/objects/%s/card" % self.kwargs.get('pk', None)

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
            # Сoздаем объекты "контакты на объекте"
            checked_contacts = request.POST.getlist('company_contact_id')
            # Удаляем контакт, если был ранее отмечен, но сейчас отметки нет
            object_contacts = ObjectContacts.objects.filter(object=object_object.pk)
            ids_to_delete = []
            ids_to_skip = []
            ids_to_add = []
            if len(checked_contacts) > 0:
                log.info("--- %s" % checked_contacts)
                for o in object_contacts:
                    log.info("--- Cheking.. object_contact id: %s checked_contacts: %s" % (o.company_contact.id, checked_contacts))
                    if str(o.company_contact.id) not in checked_contacts:
                        ids_to_delete.append(str(o.company_contact.id))
                    else:
                        ids_to_skip.append(str(o.company_contact.id))
                for item in checked_contacts:
                    if item not in ids_to_skip:
                        ids_to_add.append(item)
                log.info("--- delete: %s skip: %s add: %s" % (ids_to_delete, ids_to_skip, ids_to_add))
                if len(ids_to_delete) > 0:
                    ObjectContacts.objects.filter(object__pk=object_object.pk, company_contact__in=ids_to_delete).delete()
                if len(ids_to_add) > 0:
                    for contact_id in ids_to_add:
                        company_contact_object = CompanyContacts(pk=contact_id)
                        object_contact, created = ObjectContacts.objects.update_or_create(
                                    object=object_object,
                                    company_contact=company_contact_object,
                        )
                        object_contact.save()
            else:
                object_contacts.delete()


            # if len(checked_contacts) > 0:
            #     for contact_id in checked_contacts:
            #         company_contact_object = CompanyContacts(pk=contact_id)
            #         object_contact, created = ObjectContacts.objects.update_or_create(
            #                     object=object_object,
            #                     company_contact=company_contact_object,
            #         )
            #         object_contact.save()
            self.success_url = '/company/%s/card' % company_pk
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(forms=forms))

