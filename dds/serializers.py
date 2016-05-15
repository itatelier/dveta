# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import CompanyOrgTypes
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from company.serializers import *
from person.serializers import EmployiesSerializer, UnitGroupsSerializer



class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DdsAccounts
        depth = 1
        fields = ('pk', 'name', 'type', 'contragent', 'employee', 'balance')


class AccountsFilters(django_filters.FilterSet):

    class Meta:
        model = DdsAccounts
        fields = ['type', 'contragent', 'employee', ]


class DdsFlowSerializer(serializers.ModelSerializer):
    employee = EmployiesSerializer(many=False, read_only=True)

    class Meta:
        model = DdsFlow
        depth = 1
        fields = ('pk', 'date', 'parent_op', 'item', 'account', 'summ', 'pay_way', 'employee', 'comment')


class DdsFlowFilters(django_filters.FilterSet):

    class Meta:
        model = DdsFlow
        fields = ['item', 'account', 'summ']



