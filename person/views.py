# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404


# API
from serializers import *
from company.serializers import *
from rest_framework import viewsets, generics, filters

import logging
log = logging.getLogger('django')


class PersonCardView(LoginRequiredMixin, TemplateView):
    template_name = "person/person_card.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(PersonCardView, self).get_context_data(*args, **kwargs)
        person_pk = kwargs['pk']
        object = Persons.objects.get(pk=person_pk)
        context_data.update({
            'object': object,
            'client_contacts': CompanyContacts.objects.select_related('company', 'contact', 'contact__person').filter(contact__person__pk=person_pk),
            'contacts': Contacts.objects.select_related('person').filter(person__pk=person_pk),
            'positions': Employies.objects.select_related('person').filter(person__pk=person_pk)
        })
        return context_data


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


class EmployeeCreateView(MultiFormCreate):
    template_name = 'person/employee_create.html'
    formconf = {
        'person': {'formclass': PersonEmployeeCreateForm},
        'employee': {'formclass': EmployeeEditForm},
        }

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        pform = forms['person']
        eform = forms['employee']
        if pform.is_valid() and eform.is_valid():
            person_object = pform.save()
            employee_object = eform.save(commit=False)
            employee_object.person = person_object
            employee_object.save()
            self.success_url = '/persons/%s/card' % person_object.pk
            return HttpResponseRedirect(self.success_url)
        else:
            for form in forms:
                for field in forms[form]:
                    for err in field.errors:
                        log.warn("Field %s Err: %s" % (field.name, err))
            return self.render_to_response(self.get_context_data(forms=forms))


class EmployiesListView(LoginRequiredMixin, TemplateView):
    template_name = "person/list_employies.html"


class EployiesViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Employies.objects.filter().select_related('type', 'role', 'person')
    serializer_class = EmployiesSerializer
    # filter_class = ContragentsFilters
    search_fields = ('person__given_name', 'person__family_name', 'person__nick_name', 'comment' )
    ordering_fields = ('id', 'type', 'role', 'date_add')


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'person/person_update_info.html'
    form_class = PersonUpdateForm
    model = Persons

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        return "/persons/%s/card" % pk
