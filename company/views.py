# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone

from common.forms import *


from models import *
# from phones.models import *
# from persons.models import *
from forms import *

from django.http import HttpResponseRedirect

import logging
log = logging.getLogger('django')


class main_list_index(LoginRequiredMixin, TemplateView):
    template_name = "company/main_list_index.html"


class CompanyCreateForm(MultiFormCreate):
    template_name = 'company/company_create.html'
    success_url = '/'
    formconf = {
        'company': {'formclass': CompanyEditForm},
        # 'branch': {'formclass': BranchCompanyCreateForm},
        # 'address': {'formclass': AddressEditForm}
    }

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        cform = forms['company']
        # aform = forms['address']
        # bform = forms['branch']
        # log.info("*** Cheking form... %s" % (forms.company,))
        # log.info("*** Form is valid: .. %s" % (cform.is_valid()))
        # for err in cform.non_field_errors:
        #     log.info("*** Error: " + err)
        if cform.is_valid():
            ''' Создаем объекты первичных форм (схраняем формы)'''
            company_object = cform.save()
            # log.info("*** Form saved!")
            # Companies.objects.get(pk=2)
            # company_object.org_type = CompanyOrgTypes(pk=company_object)
            ''' Создаем объекты от зависимой формы '''
            # address_object = aform.save(commit=False)
            # branch_object = bform.save(commit=False)
            ''' Назначаем исключенные поля из созданных объектов на зависимый объект '''
            # address_object.company = company_object
            # address_object.company_main = True
            ''' Сохраняем зависимый объект '''
            # address_object.save()
            ''' Назначаем исключенные поля из созданных объектов на зависимый объект '''
            # branch_object.company = company_object
            # branch_object.address = address_object
            # branch_object.type = BranchTypes(pk=1)
            ''' Сохраняем зависимый объект '''
            # branch_object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            for form in forms:
                for field in forms[form]:
                    for err in field.errors:
                        log.warn("Field %s Err: %s" % (field.name, err))
            forms = self.get_forms()
            return self.render_to_response(self.get_context_data(forms=forms))

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(CompanyCreateForm, self).get_context_data(*args, **kwargs)
    #     context_data.update({
    #         'some_strange_variable': 42,
    #     })
    #     return context_data

    # def post(self, request, *args, **kwargs):
    #     forms = self.get_forms()
    #     cform = forms['company']
    #     aform = forms['address']
    #     bform = forms['branch']
    #     if cform.is_valid() and aform.is_valid() and bform.is_valid():
    #         ''' Создаем объекты первичных форм (схраняем формы)'''
    #         company_object = cform.save()
    #         ''' Создаем объекты от зависимой формы '''
    #         address_object = aform.save(commit=False)
    #         branch_object = bform.save(commit=False)
    #         ''' Назначаем исключенные поля из созданных объектов на зависимый объект '''
    #         address_object.company = company_object
    #         address_object.company_main = True
    #         ''' Сохраняем зависимый объект '''
    #         address_object.save()
    #         ''' Назначаем исключенные поля из созданных объектов на зависимый объект '''
    #         branch_object.company = company_object
    #         branch_object.address = address_object
    #         branch_object.type = BranchTypes(pk=1)
    #         ''' Сохраняем зависимый объект '''
    #         branch_object.save()
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         forms = self.get_forms()
    #         return self.render_to_response(self.get_context_data(forms=forms))
#
#
# class main_edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     template_name = 'company/main_edit.html'
#     permission_required = 'company.change_companies'
#     form_class = CompanyEditForm
#     model = Companies
#
#     def get_success_url(self, *args, **kwargs):
#         pk = self.kwargs.get('pk', None)
#         return "/company/%s/card" % pk
#
#
# class main_card(LoginRequiredMixin, TemplateView):
#     template_name = "company/main_card.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(main_card, self).get_context_data(*args, **kwargs)
#         object = Companies.objects.select_related('type').get(pk=kwargs['pk'])
#         context_data.update({
#             'object': object,
#             'main_phone': GetObjectOrNone(Phones, **{'company__pk': object.pk, 'company_main': True}),
#             'main_address': GetObjectOrNone(Addresses, **{'company__pk': object.pk, 'company_main': True}),
#             'branches': Branches.objects.select_related('type', 'company', 'address', 'branch_phone', 'phones').filter(company=object.pk),
#             'contragents': Contragents.objects.select_related('type').filter(company=object.pk)
#         })
#
#         return context_data
#
#
# class main_card_employees(LoginRequiredMixin, TemplateView):
#     template_name = "company/main_card_employees.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(main_card_employees, self).get_context_data(*args, **kwargs)
#         context_data.update({
#             'object': Companies.objects.select_related('type').get(pk=kwargs['pk']),
#             'employees': Employees.objects.select_related('person').filter(company=kwargs['pk'])
#         })
#
#         return context_data
#
# class main_delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView):
#     permission_required = 'company.delete_companies'
#     form_class = CompanyEditForm
#     model = Companies
#     success_url = '/company/main_list'
#     notice = 'Удаление объекта "Компания" приведет к удалению всех связанных объектов - отделений, адресов, контрагентов!'
#
#
# class branch_list_index(LoginRequiredMixin, TemplateView):
#     template_name = "company/branch_list_index.html"
#
#
# class branch_list_json(LoginRequiredMixin, JsonListMixin):
#     qs = Addresses.objects.select_related('branch', 'branch__type', 'company')
#     relations = {'branch': {'relations': ('type',), 'fields': ('id', 'name', 'type')}, 'company': {'fields': ('name',)}}
#
#     params = {
#         'page': {'required': 1, 'default': 1},
#         'rows': {'required': 1, 'default': 25},
#         'sort_col': {'required': 1, 'default': 'pk'},
#         'sort_way': {'required': 1, 'default': "-"},
#         'branch__is_active': {'type': 'bool', 'default': 'reset'},
#         'branch__type': {'type': 'filter', 'default': 'reset'},
#         'search_id': {'type': 'text', 'field': 'id', 'default': 'reset'},
#         'search_name': {'type': 'text', 'field': 'name', 'filter_type': '__icontains', 'default': 'reset'},
#         'search_company_name': {'type': 'text', 'field': 'company__name', 'filter_type': '__icontains', 'default': 'reset'},
#         'search_address_street': {'type': 'text', 'field': 'address__street', 'filter_type': '__icontains', 'default': 'reset'},
#     }
#
#
# class branch_create(MultiFormCreate):
#     template_name = 'company/branch_edit.html'
#     success_url = '/company/branch_list/'
#     formconf = {
#         'branch': {'formclass': BranchEditForm},
#         'address': {'formclass': AddressEditForm}
#     }
#
#     def post(self, request, *args, **kwargs):
#         forms = self.get_forms()
#         aform = forms['address']
#         bform = forms['branch']
#         if bform.is_valid() and aform.is_valid():
#             ''' получаем параметры из из URL, имя параметра в url.conf '''
#             company_pk = kwargs.pop('company_pk', None)
#             company_object = Companies(pk=company_pk)
#             ''' Создаем объект модели для Foreign Key '''
#             address_object = aform.save(commit=False)
#             address_object.company = company_object
#             ''' Сохраняем формы родительских объектов '''
#             address_object.save()
#             ''' Создаем объекты первичных форм, для которых добавим ключи'''
#             branch_object = bform.save(commit=False)
#             ''' Присваиваем полям зависимых форм сохраненные родительские объекты '''
#             branch_object.company = company_object
#             branch_object.address = address_object
#             ''' Сохраняем зависимые формы '''
#             branch_object.save()
#             self.success_url = '/company/%s/card' % company_pk
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             forms = self.get_forms()
#             return self.render_to_response(self.get_context_data(forms=forms))
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(branch_create, self).get_context_data(*args, **kwargs)
#         company_pk = self.kwargs.get('company_pk', None)
#         context_data.update({'company': Companies.objects.get(pk=company_pk) })
#         return context_data
#
#
# class branch_edit(MultiFormEdit):
#     template_name = 'company/branch_edit.html'
#     formconf = {
#         'branch': {'formclass': BranchEditForm},
#         'address': {'formclass': AddressEditForm}
#     }
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(branch_edit, self).get_context_data(*args, **kwargs)
#         company_pk = self.kwargs.get('company_pk', None)
#         context_data.update({'company': Companies.objects.get(pk=company_pk) })
#         return context_data
#
#     def update_formconf(self, formconf, *args, **kwargs):
#         branch_pk = kwargs.pop('pk', None)
#         branch_object = Branches.objects.get(pk=branch_pk)
#         formconf['branch']['instance'] = branch_object
#         # formconf['address']['instance'] = branch_object.addresses.get(branch__pk=branch_pk)
#         formconf['address']['instance'] = branch_object.address
#         return formconf
#
#     def get_success_url(self, *args, **kwargs):
#         company_pk = self.kwargs.get('company_pk', None)
#         branch_pk = self.kwargs.get('pk', None)
#         return "/company/%s/branch/%s/card" % (company_pk, branch_pk)
#
#
# class branch_card(LoginRequiredMixin, TemplateView):
#     template_name = "company/branch_card.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(branch_card, self).get_context_data(*args, **kwargs)
#         object = Branches.objects.select_related('type', 'company', 'address').get(pk=kwargs['pk'])
#         phones = Phones.objects.filter(branch=kwargs['pk'])
#         context_data.update({
#             'object': object,
#             'main_phone': GetObjectOrNone(Phones, **{'branch__pk': kwargs['pk'], 'branch_main': True}),
#             'phones': phones
#         })
#         return context_data
#
#
# class branch_delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView):
#     permission_required = 'company.delete_branches'
#     form_class = BranchEditForm
#     model = Branches
#     success_url = '/company/branch_list'
#     notice = 'Удаление объекта "Отделение" приведет к удалению связанного адреса!'
#
#
# class contragent_create(FormView):
#     template_name = 'company/contragent_edit.html'
#     form_class = ContragentEditForm
#
#     def get_success_url(self, *args, **kwargs):
#         company_pk = self.kwargs.get('company_pk', None)
#         return "/company/%s/card" % company_pk
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(contragent_create, self).get_context_data(*args, **kwargs)
#         company_pk = self.kwargs.get('company_pk', None)
#         context_data.update({
#             'company': Companies.objects.get(pk=company_pk),
#             'type_str': 'Юридическое лицо',
#             'type_id': 1,
#         })
#         return context_data
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form(self.form_class)
#         if form.is_valid():
#             ''' получаем параметры из из URL, имя параметра в url.conf '''
#             company_pk = kwargs.pop('company_pk', None)
#             ''' Создаем объект модели для Foreign Key '''
#             company_object = Companies(pk=company_pk)
#             type_object = ContragentTypes(pk=1)
#             ''' Создаем объекты первичных форм, для которых добавим ключи'''
#             contragent_object = form.save(commit=False)
#             ''' Присваиваем полям зависимых форм сохраненные родительские объекты '''
#             contragent_object.company = company_object
#             contragent_object.type = type_object
#             ''' Сохраняем зависимые формы '''
#             contragent_object.save()
#             self.success_url = '/company/%s/card' % company_pk
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             forms = self.get_form(self.form_class)
#             return self.render_to_response(self.get_context_data(form=form))
#
#
# class contragent_ip_create(FormView):
#     template_name = 'company/contragent_edit.html'
#     form_class = ContragentIpEditForm
#
#     def get_success_url(self, *args, **kwargs):
#         company_pk = self.kwargs.get('company_pk', None)
#         return "/company/%s/card" % company_pk
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(contragent_ip_create, self).get_context_data(*args, **kwargs)
#         company_pk = self.kwargs.get('company_pk', None)
#         context_data.update({
#             'company': Companies.objects.get(pk=company_pk),
#             'type_str': 'Индивидуальный предприниматель',
#             'type_id': 2
#         })
#         return context_data
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form(self.form_class)
#         if form.is_valid():
#             ''' получаем параметры из из URL, имя параметра в url.conf '''
#             company_pk = kwargs.pop('company_pk', None)
#             ''' Создаем объект модели для Foreign Key '''
#             company_object = Companies(pk=company_pk)
#             type_object = ContragentTypes(pk=2)
#             ''' Создаем объекты первичных форм, для которых добавим ключи'''
#             contragent_object = form.save(commit=False)
#             ''' Присваиваем полям зависимых форм сохраненные родительские объекты '''
#             contragent_object.company = company_object
#             contragent_object.type = type_object
#             ''' Сохраняем зависимые формы '''
#             contragent_object.save()
#             self.success_url = '/company/%s/card' % company_pk
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             forms = self.get_form(self.form_class)
#             return self.render_to_response(self.get_context_data(form=form))
#
#
# class contragent_edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     template_name = 'company/contragent_edit.html'
#     permission_required = 'company.change_companies'
#     model = Contragents
#
#     def get_form_class(self, *args, **kwargs):
#         type_id = self.kwargs.get('type', None)
#         form_class = None
#         ''' Если тип контрагента "ООО" - форма стандартная, если нет - ИП '''
#         if type_id == "1":
#             form_class = ContragentEditForm
#         else:
#             form_class = ContragentIpEditForm
#         return form_class
#
#     def get_success_url(self, *args, **kwargs):
#         company_pk = self.kwargs.get('company_pk', None)
#         contragent_pk = self.kwargs.get('pk', None)
#         return "/company/%s/contragent/%s/card" % (company_pk, contragent_pk)
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(contragent_edit, self).get_context_data(*args, **kwargs)
#         company_pk = self.kwargs.get('company_pk', None)
#         context_data.update({
#             'company': Companies.objects.get(pk=company_pk),
#         })
#         return context_data
#
#
# class contragent_card(LoginRequiredMixin, TemplateView):
#     template_name = "company/contragent_card.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(contragent_card, self).get_context_data(*args, **kwargs)
#         object = Contragents.objects.select_related('type', 'company').get(pk=kwargs['pk'])
#         bank_accounts = BankAccounts.objects.filter(contragent__pk=kwargs['pk'])
#         context_data.update({
#             'object': object,
#             'bank_accounts': bank_accounts
#         })
#         return context_data
#
#
# class contragent_list_index(LoginRequiredMixin, TemplateView):
#     template_name = "company/contragent_list_index.html"
#
#
# class contragent_list_json(LoginRequiredMixin, JsonListMixin):
#     qs = Contragents.objects.select_related('type', 'company__type', 'company')
#     relations = {'company': {'relations': ('type',), 'fields': ('id', 'name', 'type')}, 'type': {'fields': ('id', 'name')}}
#
#     params = {
#         'page': {'required': 1, 'default': 1},
#         'rows': {'required': 1, 'default': 25},
#         'sort_col': {'required': 1, 'default': 'pk'},
#         'sort_way': {'required': 1, 'default': "-"},
#         'type': {'type': 'filter', 'default': 'reset'},
#         'search_id': {'type': 'text', 'field': 'id', 'default': 'reset'},
#         'search_name': {'type': 'text', 'field': 'name', 'filter_type': '__icontains', 'default': 'reset'},
#         'search_inn': {'type': 'text', 'field': 'inn', 'filter_type': '__icontains', 'default': 'reset'},
#         'search_company_name': {'type': 'text', 'field': 'company__name', 'filter_type': '__шcontains', 'default': 'reset'},
#     }
#
#
# class contragent_delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView):
#     permission_required = 'company.delete_contragents'
#     form_class = ContragentEditForm
#     model = Contragents
#     notice = 'Удаление объекта "Контрагент" приведет к удалению связанных данных!'
#
#     def get_success_url(self, *args, **kwargs):
#         company_pk = self.kwargs.get('company_pk', None)
#         return "/company/%s/card" % company_pk
#
#
# class bank_account_create(FormView):
#     template_name = 'company/bank_account_edit.html'
#     form_class = BankAccountEditForm
#
#     def get_success_url(self, *args, **kwargs):
#         company_pk = self.kwargs.get('company_pk', None)
#         contragent_pk = self.kwargs.get('contragent_pk', None)
#         return "/company/%s/contragent/%s/card" % (company_pk, contragent_pk)
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(bank_account_create, self).get_context_data(*args, **kwargs)
#         company_pk = self.kwargs.get('company_pk', None)
#         contragent_pk = self.kwargs.get('contragent_pk', None)
#         context_data.update({
#             'company': Companies.objects.get(pk=company_pk),
#             'contragent': Contragents.objects.get(pk=contragent_pk),
#         })
#         return context_data
#
#     def post(self, request, *args, **kwargs):
#         form = self.get_form(self.form_class)
#         if form.is_valid():
#             ''' получаем параметры из из URL, имя параметра в url.conf '''
#             company_pk = self.kwargs.get('company_pk', None)
#             contragent_pk = kwargs.pop('contragent_pk', None)
#             ''' Создаем объект модели для Foreign Key '''
#             contragent_object = Contragents(pk=contragent_pk)
#             ''' Создаем объекты первичных форм, для которых добавим ключи'''
#             bank_account_object = form.save(commit=False)
#             ''' Присваиваем полям зависимых форм сохраненные родительские объекты '''
#             bank_account_object.contragent = contragent_object
#             ''' Сохраняем зависимые формы '''
#             bank_account_object.save()
#             self.success_url = '/company/%s/contragent/%s/card' % (company_pk, contragent_pk)
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             forms = self.get_form(self.form_class)
#             return self.render_to_response(self.get_context_data(form=form))
#
#
# class contragent_bank_card(LoginRequiredMixin, TemplateView):
#     template_name = "company/contragent_bank_card.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(contragent_bank_card, self).get_context_data(*args, **kwargs)
#         context_data.update({
#             'contragent': Contragents.objects.select_related('type', 'company').get(pk=kwargs['contragent_pk']),
#             'bank': GetObjectOrNone(BankAccounts, **{'pk': kwargs['pk']}),
#         })
#         return context_data
#
#
# class contragent_bank_edit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
#     template_name = 'company/bank_account_edit.html'
#     form_class = BankAccountEditForm
#     permission_required = 'company.change_companies'
#     model = BankAccounts
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super(contragent_bank_edit, self).get_context_data(*args, **kwargs)
#         context_data.update({
#             'contragent': Contragents.objects.select_related('type', 'company').get(pk=self.kwargs.get('contragent_pk', None)),
#         })
#         return context_data
#
#     def get_success_url(self, *args, **kwargs):
#         contragent_pk = self.kwargs.get('contragent_pk', None)
#         company_pk = self.kwargs.get('company_pk', None)
#         return "/company/%s/contragent/%s/card/" % (company_pk, contragent_pk)
#
#
# class contragent_bank_delete(LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView):
#     permission_required = 'company.delete_branches'
#     form_class = BankAccountEditForm
#     model = BankAccounts
#     success_url = '/company/branch_list'
#     notice = 'Удаление объекта "Банковский счет" приведет к удалению связанных данных!'