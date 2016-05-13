# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import CompanyOrgTypes
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from company.serializers import *


class AccountsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DdsAccounts
        depth = 1
        fields = ('pk', 'name', 'type', 'contragent', 'employee', 'balance')


class AccountsFilters(django_filters.FilterSet):

    class Meta:
        model = DdsAccounts
        fields = ['type', 'contragent', 'employee', ]


# class TypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContragentTypes
#         fields = ('pk', 'val',)
#
#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ContragentGroups
#         fields = ('pk', 'val',)
#
#
# class ContragentUlSerializer(serializers.ModelSerializer):
#     type = TypeSerializer(many=False, required=False)
#     group = GroupSerializer(many=False, required=False)
#
#     class Meta:
#         model = Contragents
#         fields = ('pk', 'company', 'name', 'type', 'group', 'inn', 'kpp', 'ogrn', 'uraddress', 'date_add', 'date_update', 'comment')
#
#
# class ContragentsFilters(django_filters.FilterSet):
#     # date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
#     # request_freq = django_filters.NumberFilter(name="client_options__request_freq")
#
#     class Meta:
#         model = Contragents
#         fields = ['id', 'name', 'company', 'type', 'group', 'inn', 'comment']



