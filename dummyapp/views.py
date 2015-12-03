from django.shortcuts import render
from django.views.generic.base import TemplateView
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
#REST
from django.contrib.auth.models import User, Group
from dummyapp.models import *
from rest_framework import viewsets
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


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = DummyCompanies.objects.all()
    serializer_class = CompanySerializer