# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from bunker.models import BunkerFlow
from object.models import ObjectTypes
from forms import *


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


class BunkerRemainsJSON(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        remains = BunkerFlow.remains.by_object_type()
        return Response(remains)


class BunkerFlowViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # queryset = BunkerFlow.objects.all()
    queryset = BunkerFlow.objects.select_related('bunker_type',
                                                 'operation_type',
                                                 'object_in',
                                                 # 'object_out',
                                                 'object_in__type',
                                                 'object_out__type',
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
                                                )
    serializer_class = BunkerFlowSerializer
    search_fields = ('object_in__name', 'object_out__name', 'object_in__company__name')
    filter_class = BunkerFlowFilters
    ordering_fields = ('bunker_type', 'operation_type', 'object_in', 'object_in_type', 'object_out', 'object_out_type', 'qty', 'date', 'object_in__company', 'operation_type' )


class BunkerFlowView(LoginRequiredMixin, TemplateView):
    template_name = "bunker/list_bunker_flow.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(BunkerFlowView, self).get_context_data(*args, **kwargs)
        context_data['bunker_type'] = BunkerTypes.objects.all()
        context_data['operation_type'] = BunkerOperationTypes.objects.all()
        return context_data


