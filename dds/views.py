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


class AccountRefillView(LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill.html'
    form_class = AccountRefillForm
    model = DdsAccounts
    # def get(self, *args, **kwargs):
    #     # form = self.form_class
    #     self.object = None
    #     # Полям формы присваивается пустой QS, что бы не тянуть всю талицу в Choices для селекта
    #     form = none_modelchoicesfields_querysets(self.form_class, ('company', ))
    #     return self.render_to_response(self.get_context_data(form=form))

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(AccountRefillView, self).get_context_data(*args, **kwargs)
    #     companny_id = self.request.POST.get('company', None)
    #     form = self.form_class
    #     # context_data.update({'formdict': "hz"})
    #     form.fields['company'].queryset = Companies.objects.filter(pk=companny_id)
    #     context_data.update({'form': form})
    #     return context_data

    def get_success_url(self):
        # return reverse('car_card', args=(self.object.id,))
        return reverse('dds_flow', args=())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = '/races/list/'
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            form = replace_form_choices_select2(form, ('company', 'contragent'))
            return self.render_to_response(self.get_context_data(form=form))


class DdsFlowView(LoginRequiredMixin,  TemplateView):
    template_name = 'dds/flow.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(DdsFlowView, self).get_context_data(*args, **kwargs)
        #context_data['bunker_types'] = BunkerTypes.objects.all()
        # context_data['company'] = Companies.objects.get(pk=company_pk)
        # context_data['bunker_types_summ'] = ('type1_summ', 'type2_summ', 'type3_summ', 'type4_summ', 'type5_summ', 'type6_summ', 'type7_summ', )
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
    ordering_fields = ('pk', 'date', 'item', 'account', 'pay_way')


class DdsOperationCard(LoginRequiredMixin, DetailView):
    template_name = "dds/dds_operation_card.html"
    model = DdsFlow
    queryset = DdsFlow.objects.select_related('item', 'account', 'account__contragent', 'account__employee__person', 'item__item_group')

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(DdsOperationCard, self).get_context_data(*args, **kwargs)
    #     context_data['bunkers_onboard'] = self.object.car_object.bunker_remain.all()
    #     # context_data['bunkers_onboard'] = BunkerFlow.remains.by_object_id(self.object.car_object_id)
    #     # context_data['bunkers_onboard'] = BunkerFlow.objects.filter(object__pk=self.object.car_object.id).aggregate(Sum('qty'))
    #     return context_data
