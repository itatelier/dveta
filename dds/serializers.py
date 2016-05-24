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
    employee = EmployiesSerializer(many=False, read_only=True)

    class Meta:
        model = DdsAccounts
        depth = 1
        fields = ('pk', 'name', 'type', 'contragent', 'employee', 'balance', 'status')


class AccountsSerializerShort(serializers.ModelSerializer):

    class Meta:
        model = DdsAccounts
        depth = 1
        fields = ('pk', 'name', 'type', 'balance', 'status')


class AccountsFilters(django_filters.FilterSet):

    class Meta:
        model = DdsAccounts
        fields = ['id', 'type', 'contragent', 'employee', 'status', 'contragent__company']


class DdsFlowSerializer(serializers.ModelSerializer):
    employee = EmployiesSerializer(many=False, read_only=True)
    account = AccountsSerializerShort(many=False, read_only=True)

    class Meta:
        model = DdsFlow
        depth = 1
        fields = ('pk', 'date', 'parent_op', 'item', 'account','account', 'summ', 'pay_way', 'employee', 'comment')


class DdsFlowFilters(django_filters.FilterSet):
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date", lookup_type='gte')
    date_before = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date", lookup_type='lte')

    class Meta:
        model = DdsFlow
        fields = ['item', 'account', 'summ', 'item__item_group', 'date_after', 'date_before', 'pay_way']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = DdsItems
        depth = 1
        fields = ('pk', 'name', 'direction_type', 'item_group', )


class ItemFilters(django_filters.FilterSet):
    class Meta:
        model = DdsItems
        fields = ['id', 'direction_type', 'item_group', ]
