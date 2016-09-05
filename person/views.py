# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *
from common.mixins import JsonViewMix
from datetime import datetime


# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix, JsonUpdateObject
from django.http import HttpResponse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist


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
            'positions': Employies.objects.select_related('person', 'role', 'type').filter(person__pk=person_pk)
        })
        # Контакты
        contacts_list = Contacts.objects.select_related('person').filter(person__pk=person_pk)
        if len(contacts_list) >= 1:
            context_data['contacts'] = contacts_list
        return context_data


class EmployeeUpdateSalaryView(LoginRequiredMixin, UpdateView):
    template_name = 'person/employee_update_salary.html'
    form_class = EmployeeUpdateSalaryForm
    model = Employies

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        return "/persons/employee/%s/salary/settings" % pk

    def get_context_data(self, **kwargs):
        context_data = super(EmployeeUpdateSalaryView, self).get_context_data(**kwargs)
        live_jormal = LiveOnbaseJornal.objects.filter(employee=self.kwargs.get('pk'))
        if len(live_jormal) > 0 and live_jormal.last().is_closed == False:
            context_data['is_live_now'] = True
        context_data['live_onbase_jornal'] = live_jormal
        return context_data


class EmployeeCardView(LoginRequiredMixin, TemplateView):
    template_name = "person/employee_card.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(EmployeeCardView, self).get_context_data(*args, **kwargs)
        object_pk = kwargs['pk']
        object = Employies.objects.select_related('person', 'type', 'role').get(pk=object_pk)
        context_data['object'] = object
        contacts_list = Contacts.objects.select_related('person').filter(person__pk=object.person.pk)
        if len(contacts_list) >= 1:
            context_data['contacts'] = contacts_list
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
            employee_object.status = EmployeeStatuses.objects.get(pk=1)
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

    def get_context_data(self, *args, **kwargs):
        context_data = super(EmployiesListView, self).get_context_data(*args, **kwargs)
        context_data.update({
            'status_options': EmployeeStatuses.objects.all()
        })
        return context_data


class EployiesViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Employies.objects.filter().select_related('type', 'role', 'person', 'status')
    serializer_class = EmployiesSerializer
    filter_class = EmployiesFilters
    search_fields = ('person__given_name', 'person__family_name', 'person__nick_name', 'comment')
    ordering_fields = ('id', 'type', 'role', 'date_add', 'status', 'person__nick_name', 'person__family_name')


class PersonUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'person/person_update_info.html'
    form_class = PersonUpdateForm
    model = Persons

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        return "/persons/%s/card" % pk


class PersonContactsUpdateView(LoginRequiredMixin, CreateView):
    template_name = 'person/person_contacts_update.html'
    form_class = ContactCreateForm
    success_url = ''
    queryset = Contacts.objects.all()

    def get_context_data(self, *args, **kwargs):
        context_data = super(PersonContactsUpdateView, self).get_context_data(*args, **kwargs)
        person_pk = self.kwargs.get('pk', None)
        context_data.update({
            'object': Persons.objects.get(pk=person_pk),
            'contacts': Contacts.objects.select_related('person').filter(person__pk=person_pk),
        })
        return context_data

    def post(self, request, *args, **kwargs):
        person_pk = self.kwargs.get('pk', None)
        form = self.get_form()
        if form.is_valid():
            person_object = Persons.objects.get(pk=person_pk)
            contact_object = form.save(commit=False)
            contact_object.person = person_object
            contact_object.save()
            self.success_url = '/persons/%s/contacts' % person_pk
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            for field in form:
                for err in field.errors:
                    log.warn("Field %s Err: %s" % (field.name, err))
            return self.render_to_response(self.get_context_data(form=form))


class ContactDeleteView(LoginRequiredMixin, DeleteNoticeView):
    model = Contacts
    notice = 'Восстановление контактной информации персоны невозможно!'

    def get_success_url(self, *args, **kwargs):
        person_pk = self.kwargs.get('person_pk', None)
        return reverse('person_card', args=(person_pk,))


class ContactSetMainView(JsonUpdateObject):
    model_name = 'person.Contacts'
    inicial_data = {'colname': 'is_main'}

    def get(self, request, *args, **kwargs):
        person_pk = self.kwargs.get('person_pk', None)
        if self.check_required_params(self.required_params):
            all_contacts = Contacts.objects.filter(person__pk=person_pk)
            all_contacts.update(**{'is_main': False})
            self.update_data['value'] = True
            self.update_object(request, self.update_data)
        return HttpResponse(self.to_json(self.json), )


class UpdateLiveOnbaseStatus(JsonViewMix):
    param_names = ['action', 'employee_pk']
    model = LiveOnbaseJornal

    def prepare(self, *args, **kwargs):
        # Првоеряем статус
        jornal_object = None
        action = self.values['action']
        employe_pk = self.values['employee_pk']
        try:
            jornal_object = self.model.objects.get(employee=employe_pk, is_closed=False)
        except ObjectDoesNotExist:
            pass
        if action == "on":
            if jornal_object:
                self.errors.append("Employee already in Live status")
                return
            else:
                employee_object = Employies(pk=employe_pk)
                create_object = self.model(employee=employee_object)
                create_object.save()
                return
        elif action == "off":
            if not jornal_object:
                self.errors.append("Jornal status not found for employee")
                return
            else:
                jornal_object.date_closed = datetime.now()
                jornal_object.is_closed = True
                jornal_object.save()
            return

