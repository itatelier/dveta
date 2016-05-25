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
    form_class = AccountRefillSimpleForm
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
    form_class = AccountRefillSimpleForm
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
    form_class = AccountRefillSimpleForm
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

