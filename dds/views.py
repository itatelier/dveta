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


class DdsFlowView(LoginRequiredMixin,  TemplateView):
    template_name = 'dds/dds_flow.html'

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
    success_url = '/dds/templates/group/0/'


class DdsTemplatesListView(LoginRequiredMixin,  TemplateView):
    template_name = 'dds/dds_templates_list.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(DdsTemplatesListView, self).get_context_data(*args, **kwargs)
        list_templates_qs = DdsTemplates.objects.select_related('group', 'item_in', 'item_out')
        list_groups_qs = DdsTemplateGroups.objects.all()
        group_id = self.kwargs.get('group_id', "")
        if int(group_id) > 0:
            list_templates_qs.filter(group=group_id)
            list_groups_qs.filter(pk=group_id)
            context_data['selected_group'] = DdsTemplateGroups.objects.get(pk=group_id)
        context_data['templates'] = list_templates_qs
        context_data['groups'] = list_groups_qs
        return context_data


class DdsTemplateDeleteView(LoginRequiredMixin, DeleteNoticeView):
    # permission_required = 'company.delete_branches'
    model = DdsTemplates
    success_url = '/dds/templates/group/0/'
    notice = 'Восстановление шаблона финансовой операции невозможно!'


class DdsTemplateOperation(MultiFormCreate):
    template_name = 'dds/dds_operation_from_template.html'
    success_url = '/dds/flow/'
    formconf = {
        'outop': {'formclass': DdsOperationAccountFormOut},
        'inop': {'formclass': DdsOperationAccountFormIn},
        'details': {'formclass': DdsOperationDetailsForm}
    }

    def get(self, request, *args, **kwargs):
        forms = self.get_forms()
        # Загружаем объект шаблона
        template_object = DdsTemplates.objects.get(pk=kwargs.pop('template_id', None))
        initial_out = {}
        initial_in = {}
        initial_details = {}
        # Передача параметров в форму из урла
        if request.GET.get('account_out'):
            initial_out['account'] = request.GET.get('account_out')
        if request.GET.get('account_in'):
            initial_in['account'] = request.GET.get('account_in')
        # Если в шаблоне стоит флаг _required для поля формы - обновляем значение поля формы, если оно тоже есть
        if template_object.account_out_required:
            # Передаем параметры в виджеты, что бы корректно работали функции во фронте
            # -- Статья Расход --
            forms['outop'].fields['item_groups'].widget.attrs = {"rel": "select_group",  'data-combined-id': "id_outop-item"}
            forms['outop'].fields['item'].required = True
            ''' В моделе обязательно должно для полей быть выставлено null=True, blank=True, иначе проверку на if template_object.поле выдаст ошибку'''
            if template_object.item_out:
                log.info("--- obj item_out: %s" % template_object.item_out)
                initial_out['item'] = template_object.item_out.pk
            # -- Счет расхода --
            forms['outop'].fields['account'].required = True
            if template_object.account_out:
                initial_out['account'] = template_object.account_out.pk
        forms['outop'].initial = initial_out
        # Форма операции прихода
        if template_object.account_in_required:
            # -- Статья Приход --
            forms['inop'].fields['item'].required = True
            forms['inop'].fields['item_groups'].widget.attrs = {"rel": "select_group",  'data-combined-id': "id_inop-item"}
            if template_object.item_in:
                initial_in['item'] = template_object.item_in.pk
            # -- Счет Приход --
            forms['inop'].fields['account'].required = True
            if template_object.account_in:
                initial_in['account'] = template_object.account_in.pk
        forms['inop'].initial = initial_in
        # Форма параметров операции
        if template_object.summ:
            initial_details['summ'] = int(template_object.summ)
        if template_object.comment:
            initial_details['comment'] = template_object.comment
        if template_object.pay_way is not None:
            initial_details['pay_way'] = template_object.pay_way
        forms['details'].initial = initial_details
        return self.render_to_response(self.get_context_data(forms=forms, template=template_object))

    def post(self, request, *args, **kwargs):
        forms = self.get_forms()
        outform = forms['outop']
        inform = forms['inop']
        details_form = forms['details']
        template_object = DdsTemplates.objects.get(pk=kwargs.pop('template_id', None))
        if outform.is_valid() and inform.is_valid() and details_form.is_valid():
            details_object = details_form.save(commit=False)
            if template_object.account_out_required:
                out_operation = outform.save(commit=False)
                out_operation.summ = details_object.summ
                out_operation.op_type = False
                out_operation.pay_way = details_object.pay_way
                out_operation.comment = details_object.comment
                # Обновляем баланс счета на положительную сумму
                DdsAccounts.objects.update_balance(out_operation.account.pk, abs(out_operation.summ)*-1)
                out_operation.save()
            if template_object.account_in_required:
                in_operation = inform.save(commit=False)
                in_operation.summ = details_object.summ
                in_operation.op_type = True
                in_operation.pay_way = details_object.pay_way
                in_operation.comment = details_object.comment
                # Обновляем баланс счета на отрицатульную сумму
                DdsAccounts.objects.update_balance(in_operation.account.pk, abs(in_operation.summ))
                in_operation.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            forms = self.get_forms()
            return self.render_to_response(self.get_context_data(forms=forms, template=template_object))

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(DdsTemplateOperation, self).get_context_data(*args, **kwargs)
    #     # company_pk = self.kwargs.get('company_pk', None)
    #     # context_data.update({'company': Companies.objects.get(pk=company_pk)})
    #     return context_data
