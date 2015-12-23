# -*- coding: utf8 -*

# App spcific
from models import *
from forms import *
from company.models import *

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


class ContragentCompanyCreateULView(FormView):
    template_name = 'contragent/contragent_create_ul.html'
    form_class = ContragentUlEditForm
    contragent_type = 2
    contragent_group = 4
    type_str = 'Юридическое лицо'

    def get_success_url(self, *args, **kwargs):
        company_pk = self.kwargs.get('company_pk', None)
        return "/company/%s/card" % company_pk

    def get_context_data(self, *args, **kwargs):
        context_data = super(ContragentCompanyCreateULView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        context_data.update({
            'company': Companies.objects.get(pk=company_pk),
            'type_str': self.type_str,
            'type_id': self.contragent_type,
            'contragent_group': self.contragent_group
        })
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        if form.is_valid():
            ''' получаем параметры из из URL, имя параметра в url.conf '''
            company_pk = kwargs.pop('company_pk', None)
            ''' Создаем объект модели для Foreign Key '''
            company_object = Companies(pk=company_pk)
            type_object = ContragentTypes(pk=self.contragent_type)
            group_object = ContragentGroups(pk=self.contragent_group)
            ''' Создаем объекты первичных форм, для которых добавим ключи'''
            contragent_object = form.save(commit=False)
            ''' Присваиваем полям зависимых форм сохраненные родительские объекты '''
            contragent_object.company = company_object
            contragent_object.group = group_object
            contragent_object.type = type_object
            ''' Сохраняем зависимые формы '''
            contragent_object.save()
            self.success_url = '/company/%s/card' % company_pk
            return HttpResponseRedirect(self.get_success_url())
        else:
            ''' Форма не прошла валидацию, выводим повторно'''
            forms = self.get_form(self.form_class)
            return self.render_to_response(self.get_context_data(form=form))


class ContragentCompanyCreateIPView(ContragentCompanyCreateULView):
    template_name = 'contragent/contragent_create_ul.html'
    form_class = ContragentIpEditForm
    contragent_type = 3
    contragent_group = 4
    type_str = 'Индивидуальный предприниматель'


class ContragentCompanyUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'contragent/contragent_create_ul.html'
    # permission_required = 'company.change_companies'
    model = Contragents

    def get_form_class(self, *args, **kwargs):
        type_id = self.kwargs.get('type', None)
        form_class = None
        ''' Если тип контрагента "ООО" - форма стандартная, если нет - ИП '''
        if type_id == "2":
            form_class = ContragentUlEditForm
        elif type_id == "3":
            form_class = ContragentIpEditForm
        else:
            form_class = ContragentFlEditForm
        return form_class

    def get_success_url(self, *args, **kwargs):
        company_pk = self.kwargs.get('company_pk', None)
        contragent_pk = self.kwargs.get('pk', None)
        return "/company/%s/card" % company_pk

    def get_context_data(self, *args, **kwargs):
        context_data = super(ContragentCompanyUpdateView, self).get_context_data(*args, **kwargs)
        company_pk = self.kwargs.get('company_pk', None)
        context_data.update({
            'company': Companies.objects.get(pk=company_pk),
        })
        return context_data


class ContragentsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Contragents.objects.filter(group=4).select_related('type', 'group',)
    serializer_class = ContragentUlSerializer
    filter_class = ContragentsFilters
    search_fields = ('name', 'inn', 'comment', 'urraddress', )
    ordering_fields = ('id', 'name', 'company', 'type', 'group', 'inn')


# class GetContactViewSet(viewsets.ModelViewSet):
#     filter_backends = (filters.DjangoFilterBackend,)
#     queryset = CompanyContacts.objects.select_related('company', 'contact', 'contact__person')
#     serializer_class = CompanyContactsSerializerShort
#     filter_class = CompanyContactsFilters
#
#
# class CreateCompanyContactJsonView(JsonViewMix):
#     param_names = ['company_id', 'contact_id']
#     login_required = True
#
#     def prepare(self, *args, **kwargs):
#         find_filters = {
#             'company_id': self.values['company_id'],
#             'contact_id': self.values['contact_id']
#         }
#
#         company_contact_exist_object = CompanyContacts.objects.filter(**find_filters)
#         if company_contact_exist_object:
#             self.errors.append("Контакт уже связан с компанией!")
#         else:
#             company_contact_object = CompanyContacts.objects.create(
#                 company_id=self.values['company_id'],
#                 contact_id=self.values['contact_id']
#             )
#             company_contact_object.save()
#             self.values['Success'] = 'true'
#             log.info("New object saved")
#         return