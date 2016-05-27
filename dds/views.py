# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone
from django.shortcuts import get_object_or_404
from common.forms import *


from models import *
# from phones.models import *
from person.forms import *
from forms import *
from serializers import *
from contragent.models import *
from rest_framework import viewsets, generics, filters
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView


class AccountsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = DdsAccounts.objects.select_related(
        'type',
        'contragent',
        'employee',
    ).prefetch_related(
        'employee__person'
    )
    serializer_class = AccountsSerializer
    search_fields = ('name', 'contragent_name', 'employee__person__family_name')
    filter_class = AccountsFilters
    ordering_fields = ('pk', 'contragent__name', 'balance', 'name', 'type')


class AccountsBalanceView(LoginRequiredMixin,  TemplateView):
    template_name = 'dds/accounts_balance.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(AccountsBalanceView, self).get_context_data(*args, **kwargs)
        context_data['account_types'] = DdsAccountTypes.objects.all()
        return context_data


class AccountRefillContragentView(LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill_contragent.html'
    form_class = AccountRefillContragentForm
    model = DdsAccounts

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()

            # Обновление баланса счета
            DdsAccounts.objects.update_balance(pk=new_object.account.id, summ=new_object.summ)

            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            form = replace_form_choices_select2(form, ('company', 'contragent'))
            return self.render_to_response(self.get_context_data(form=form))


class AccountRefillEmployeeView(LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill_employee.html'
    form_class = AccountRefillEmployeeForm

    def get_context_data(self, *args, **kwargs):
        context_data = super(AccountRefillEmployeeView, self).get_context_data(*args, **kwargs)
        #context_data['form'].fields['comment'].initial = "TEST"

        context_data['form'].initial = {
            'employee': 1
        }
        return context_data


    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()

            # Обновление баланса счета
            DdsAccounts.objects.update_balance(pk=new_object.account.id, summ=new_object.summ)

            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            form = replace_form_choices_select2(form, formfields=('employee', ))
            return self.render_to_response(self.get_context_data(form=form))


class AccountRefillCashView(LoginRequiredMixin, CreateView):
    # родительский класс для форм с типом счета 1,2,3 - следующие View: AccountRefillBankView, AccountRefillServiceView
    template_name = 'dds/account_refill_simple.html'
    form_class = DdsOperationForm
    account_type = 1
    menu_item = 1

    def get_context_data(self, *args, **kwargs):
        context_data = super(AccountRefillCashView, self).get_context_data(*args, **kwargs)
        context_data['accounts'] = DdsAccounts.objects.filter(type=self.account_type)
        context_data['menu_item'] = self.menu_item
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()

            # Обновление баланса счета
            DdsAccounts.objects.update_balance(pk=new_object.account.id, summ=new_object.summ)

            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class AccountRefillBankView(AccountRefillCashView, LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill_simple.html'
    form_class = DdsOperationForm
    account_type = 2
    menu_item = 2

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class AccountRefillServiceView(AccountRefillCashView, LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill_simple.html'
    form_class = DdsOperationForm
    account_type = 3
    menu_item = 3

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class DdsFlowView(LoginRequiredMixin,  TemplateView):
    template_name = 'dds/flow.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(DdsFlowView, self).get_context_data(*args, **kwargs)
        context_data['item_groups'] = DdsItemGroups.objects.all()
        context_data['selected_account'] = self.kwargs.get('account_id', "")
        return context_data


class DdsFlowViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = DdsFlow.objects.select_related(
        'account',
        'item',
        'account__type'
    )
    serializer_class = DdsFlowSerializer
    search_fields = ('comment', )
    filter_class = DdsFlowFilters
    ordering_fields = ('pk', 'date', 'item', 'summ', 'account', 'pay_way', 'account__name', 'account__type')
    ordering = ('-pk',)


class DdsOperationCard(LoginRequiredMixin, DetailView):
    template_name = "dds/dds_operation_card.html"
    model = DdsFlow
    queryset = DdsFlow.objects.select_related('item', 'account', 'account__contragent', 'account__employee__person', 'item__item_group')


class DdsItemsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    queryset = DdsItems.objects.select_related('item_group', )
    serializer_class = ItemSerializer
    filter_class = ItemFilters
    ordering = ('direction_type',)


class DdsTemplateCreateView(LoginRequiredMixin, CreateView):
    template_name = 'dds/dds_template_create.html'
    form_class = DdsTemplateForm
    success_url = '/dds/flow/'


class DdsTemplateOperation(MultiFormCreate):
    template_name = 'dds/dds_operation_from_template.html'
    success_url = '/dds/flow/'
    formconf = {
        'outop': {'formclass': DdsOperationAccountForm},
        'inop': {'formclass': DdsOperationAccountForm},
        'details': {'formclass': DdsOperationDetailsForm}
    }

    def get(self, request, *args, **kwargs):
        forms = self.get_forms()
        # Загружаем объект шаблона
        template_object = DdsTemplates.objects.get(pk=kwargs.pop('template_id', None))
        initial_out = {}
        initial_in = {}
        initial_details = {}
        # Если в шалоне стоит флаг _required для поля формы - обновляем значение поля формы, если оно тоже есть
        if template_object.account_out_required:
            # Передаем параметры в виджеты, что бы корректно работали функции во фронте
            # -- Статья Расход --
            forms['outop'].fields['item_groups'].widget.attrs = {"rel": "select_group",  'data-combined-id': "id_outop-item"}
            forms['outop'].fields['item'].required = True
            if hasattr(template_object, 'item_out'):
                initial_out['item'] = template_object.item_out.pk
                forms['outop'].fields['item'].widget.attrs.update({"disabled": True})
            # -- Счет расхода --
            forms['outop'].fields['account'].required = True
            if hasattr(template_object, 'account_out'):
                initial_out['account'] = template_object.account_out.pk
        forms['outop'].initial = initial_out
        # Форма операции прихода
        if template_object.account_out_required:
            # -- Статья Приход --
            forms['inop'].fields['item'].required = True
            forms['inop'].fields['item_groups'].widget.attrs = {"rel": "select_group",  'data-combined-id': "id_inop-item"}
            if hasattr(template_object, 'item_in'):
                forms['inop'].fields['item'].widget.attrs.update({"disabled": True})
                initial_in['item'] = template_object.item_in.pk
            # -- Счет Приход --
            forms['inop'].fields['account'].required = True
            if hasattr(template_object, 'account_in'):
                initial_in['account'] = template_object.account_in.pk
        forms['inop'].initial = initial_in
        # Форма параметров операции
        if hasattr(template_object, 'summ'):
            initial_details['summ'] = int(template_object.summ)
        if hasattr(template_object, 'comment'):
            initial_details['comment'] = template_object.comment
        if hasattr(template_object, 'pay_way'):
            initial_details['pay_way'] = template_object.pay_way
        forms['details'].initial = initial_details
        return self.render_to_response(self.get_context_data(forms=forms, template=template_object))

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        outform = forms['outop']
        inform = forms['inop']
        details_form = forms['details']

        if outform.is_valid() and inform.is_valid() and details_form.is_valid():
            # company_pk = kwargs.pop('company_pk', None)
            # company_object = Companies(pk=company_pk)
            # address_object = aform.save()
            # branch_object = bform.save(commit=False)
            # branch_object.company = company_object
            # branch_object.address = address_object
            # branch_object.save()
            # self.success_url = '/company/%s/card' % company_pk
            return HttpResponseRedirect(self.get_success_url())
        else:
            template_object = DdsTemplates.objects.get(pk=kwargs.pop('template_id', None))
            forms = self.get_forms()
            # return self.get(self, request, template_id=kwargs.pop('template_id', None))
            return self.render_to_response(self.get_context_data(forms=forms, template=template_object))

    def get_context_data(self, *args, **kwargs):
        context_data = super(DdsTemplateOperation, self).get_context_data(*args, **kwargs)
        # company_pk = self.kwargs.get('company_pk', None)
        # context_data.update({'company': Companies.objects.get(pk=company_pk)})
        return context_data
