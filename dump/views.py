# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix, JsonUpdateObject
from django.http import HttpResponse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, Func, F



# API
from serializers import *
from company.serializers import *
from rest_framework import viewsets, generics, filters

import logging
log = logging.getLogger('django')


class TalonsFlowView(LoginRequiredMixin, TemplateView):
    template_name = "dump/talons_flow.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(TalonsFlowView, self).get_context_data(*args, **kwargs)
        context_data.update({
            'dump_groups': DumpGroups.objects.all()
        })
        return context_data


class TalonsFlowViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = TalonsFlow.objects.filter().select_related('dump_group', 'employee', 'employee__person')
    serializer_class = TalonsFlowSerializer
    filter_class = TalonsFlowFilters
    search_fields = ('comment', )
    ordering_fields = ('id', 'operation_type', 'dump_group', )


class TalonsMoveBuyView(LoginRequiredMixin, CreateView):
    template_name = 'dump/talons_move_buy.html'
    form_class = TalonsMoveBuyForm
    success_url = '/dump/talons_flow'
    queryset = TalonsFlow.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            flow_object = form.save(commit=False)
            flow_object.operation_type = 0
            flow_object.sum = flow_object.qty * flow_object.price
            # flow_object.paid_qty = flow_object.sum_paid / flow_object.price
            flow_object.save()
            self.success_url = '/'
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class TalonsMoveBetweenView(LoginRequiredMixin, CreateView):
    template_name = 'dump/talons_move_between.html'
    form_class = TalonsMoveBetweenForm
    success_url = '/dump/talons_flow'
    queryset = TalonsFlow.objects.all()
    employee_from_pk = False
    employee_to_pk = False

    def dispatch(self, request, *args, **kwargs):
        self.employee_from_pk = request.GET.get('employee_from', False)
        self.employee_to_pk = request.GET.get('employee_to', False)
        return super(TalonsMoveBetweenView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return reverse('/')

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        # Передача параметров в форму из урла
        initial = {}
        data = {}    # Данные для контекста шаблона
        if self.employee_from_pk:
            initial['employee_from'] = self.employee_from_pk
            form.fields['employee_from'].widget = widgets.HiddenInput()
            data['employee_from'] = Employies.objects.select_related('person').get(pk=self.employee_from_pk)
        if self.employee_to_pk:
            initial['employee_to'] = self.employee_to_pk
            form.fields['employee_to'].widget = widgets.HiddenInput()
            data['employee_to'] = Employies.objects.select_related('person').get(pk=self.employee_to_pk)
        form.initial = initial
        return self.render_to_response(self.get_context_data(form=form, data=data))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # выясняем группу тулонодержателей
        if 'employee_from' in form.data:
            self.employee_from_pk = form.data['employee_from']
        employee_out_role = Employies.objects.get(pk=self.employee_from_pk).role.pk
        employee_in_role = Employies.objects.get(pk=form.data['employee_to']).role.pk
        employee_out_group = 0
        employee_in_group = 0
        if employee_out_role == 2:
            employee_out_group = 1
        if employee_in_role == 2:
            employee_in_group = 1
        # выполняем процедуру перемещения
        proc_result, proc_error = TalonsFlow.objects.move_between_proc(
            3, # тип операции ПЕРЕДАЧА
            form.data['dump_group'],
            form.data['qty'],
            self.employee_from_pk,
            form.data['employee_to'],
            employee_out_group,
            employee_in_group
        )
        # если ессть ошибкив  процедуре добавляем ошибку в форму
        if proc_result != 1:
            form.add_error(None, proc_error)
        if form.is_valid():
            self.success_url = reverse('talons_flow')
            return HttpResponseRedirect(self.success_url)
        else:
            data = {}  # Данные для контекста шаблона
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class TalonsReportRemainsByGroup(TemplateView):
    template_name = 'dump/talons_report_remains_bygroup.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(TalonsReportRemainsByGroup, self).get_context_data(*args, **kwargs)
        tqty = Sum(Func('remains', function='IFNULL', template='%(function)s(%(expressions)s,qty)'))
        context_data.update({
            #'report_data': TalonsFlow.objects.filter(is_closed__isnull=True).exclude(operation_type__in=(1, 2)).values('employee_group',).annotate(remains=tqty)
            'report_by_dump_group' : TalonsFlow.objects.report_by_dump_group()
        })
        return context_data
