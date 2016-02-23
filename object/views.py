# -*- coding: utf8 -*

# App spcific
from models import *


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


class ObjectsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Objects.objects.select_related('type', 'company', 'address', 'company__client_options', 'company__status', 'company__org_type', 'company__rel_type')
    serializer_class = ObjectsSerializer
    search_fields = ('name', 'company__name', 'address__street')
    filter_class = ObjectFilters
    ordering_fields = ('type',)