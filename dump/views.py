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
