# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from bunker.models import BunkerFlow
from object.models import ObjectTypes
from forms import *
from common.utils import get_attr_or_null


# API
from serializers import *
from person.serializers import *
from rest_framework import viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.db.models import Sum
from django.shortcuts import get_object_or_404

import logging
log = logging.getLogger('django')





class BunkerRemainsJSON(APIView):
    # REST View с выводом из RAW SQL хранимым в менеджере моделей
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        # result = BunkerFlow.objects.list_flow()
        result = BunkerFlow.objects.move_bunker_between_objects(1, 2, 1, 2)
        log.info("--- Result: %s" % result)
        return Response(result)


class BunkerFlowRemainsReportView(LoginRequiredMixin, TemplateView):
    template_name = "bunker/report_flow.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(BunkerFlowRemainsReportView, self).get_context_data(*args, **kwargs)
        context_data['result_by_status'] = BunkerFlow.remains.by_company_status()
        context_data['result_by_object_type'] = BunkerFlow.remains.by_object_type()
        return context_data


class BunkerFlowViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # queryset = BunkerFlow.objects.all()
    queryset = BunkerFlow.objects.select_related('bunker_type',
                                                 'operation_type',
                                                 'object_in',
                                                 # 'object_out',
                                                 'object_out',
                                                 # 'object_in__company',
                                                 # 'object_in__company__status',
                                                 # 'object_out__company',
                                                 ).prefetch_related(
                                                 'object_in__company',
                                                 'object_in__company__status',
                                                 'object_in__company__client_options',
                                                 'object_in__company__org_type',
                                                 'object_out__company',
                                                 'object_out__company__status',
                                                 'object_out__company__client_options',
                                                 'object_out__company__org_type',
                                                ).order_by('-id')
    serializer_class = BunkerFlowSerializer
    search_fields = ('object_in__name', 'object_out__name', 'object_in__company__name')
    filter_class = BunkerFlowFilters
    ordering_fields = ('id', 'bunker_type', 'operation_type', 'object_in', 'object_in__type', 'object_out', 'object_out__type', 'qty', 'date', 'object_in__company', 'operation_type' )


class BunkerFlowView(LoginRequiredMixin, TemplateView):
    template_name = "bunker/list_bunker_flow.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(BunkerFlowView, self).get_context_data(*args, **kwargs)
        context_data['bunker_type'] = BunkerTypes.objects.all()
        context_data['operation_type'] = BunkerOperationTypes.objects.all()
        return context_data


class BunkerOperationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'bunker/bunker_flow_add_operation.html'
    form_class = BunkerFlowForm
    model = BunkerFlow

    def get_success_url(self):
        return reverse('bunker_flow')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            operation_type = get_attr_or_null(form.cleaned_data['operation_type'], 'pk')
            object_out_id = get_attr_or_null(form.cleaned_data['object_out'], 'pk')
            object_in_id = get_attr_or_null(form.cleaned_data['object_in'], 'pk')
            bunker_type = get_attr_or_null(form.cleaned_data['bunker_type'], 'pk')
            qty = form.cleaned_data['qty']
            # вызов процедуры перемещения между бункерами
            result = BunkerFlow.objects.move_bunker_between_objects(operation_type, object_out_id, object_in_id, bunker_type, qty)
            return HttpResponseRedirect(reverse('bunker_flow'))
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))