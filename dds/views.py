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
    ordering_fields = ('pk', 'contragent__name', 'balance')


class AccountRefillContragentView(LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill_contragent.html'
    form_class = AccountRefillContragentForm
    model = DdsAccounts

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            form = replace_form_choices_select2(form, ('company', 'contragent'))
            return self.render_to_response(self.get_context_data(form=form))


class AccountRefillEmployeeView(LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill_employee.html'
    form_class = AccountRefillEmployeeForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = reverse('dds_operation_card', args=(new_object.id,))
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            form = replace_form_choices_select2(form, ('employee', ))
            return self.render_to_response(self.get_context_data(form=form))


class DdsFlowView(LoginRequiredMixin,  TemplateView):
    template_name = 'dds/flow.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(DdsFlowView, self).get_context_data(*args, **kwargs)
        context_data['item_groups'] = DdsItemGroups.objects.all()
        return context_data


class DdsFlowViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = DdsFlow.objects.select_related(
        'account',
        'item',
    ).prefetch_related(
        'account__employee__person'
    )
    serializer_class = DdsFlowSerializer
    search_fields = ('comment', )
    filter_class = DdsFlowFilters
    ordering_fields = ('pk', 'date', 'item', 'summ', 'account', 'pay_way', 'account__contragent', 'account__employee')


class DdsOperationCard(LoginRequiredMixin, DetailView):
    template_name = "dds/dds_operation_card.html"
    model = DdsFlow
    queryset = DdsFlow.objects.select_related('item', 'account', 'account__contragent', 'account__employee__person', 'item__item_group')
