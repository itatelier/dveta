from django.shortcuts import render
from django.views.generic.base import TemplateView
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
#REST
from django.contrib.auth.models import User, Group
from dummyapp.models import *
from rest_framework import viewsets, generics, filters
import django_filters
from dummyapp.serializers import UserSerializer, GroupSerializer, CompanySerializer


import logging
log = logging.getLogger('django')


class DummyListingIndex(LoginRequiredMixin, TemplateView):
    template_name = "dummy/listing.html"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CompanyFilters(django_filters.FilterSet):
    name_ac = django_filters.CharFilter(name="name", lookup_type='icontains')
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')

    class Meta:
        model = DummyCompanies
        fields = ['name', 'date_after', 'name_ac']


class CompanyViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
    queryset = DummyCompanies.objects.all()
    serializer_class = CompanySerializer
    filter_class = CompanyFilters
    search_fields = ('www', 'description')
