# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import CompanyOrgTypes
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters


class OrgTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyOrgTypes
        fields = ('pk', 'val',)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyStatus
        fields = ('pk', 'val',)


class RelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRelTypes
        fields = ('pk', 'val',)


class AttrSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyRelTypes
        fields = ('pk', 'val',)


class ClientOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOptions
        fields = ('pk', 'request_tickets', 'request_special_sign', 'request_freq', 'use_client_talons_only', 'pay_condition', 'pay_type', 'credit_limit')


class CompanyClientsSerializer(serializers.ModelSerializer):
    # pk = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    # description = serializers.CharField(required=False, allow_blank=True, max_length=255)
    # www = serializers.CharField(required=False, allow_blank=True, max_length=250)
    org_type = OrgTypeSerializer(many=False, required=False)
    status = StatusSerializer(many=False, required=False)
    client_options = ClientOptionsSerializer(many=False, required=False)
    # request_freq = ClientOptionsSerializer(many=False, read_only=True,)
    # rel_type = serializers.BooleanField(required=True)
    # date_add = serializers.DateTimeField(required=True)

    class Meta:
        model = Companies
        fields = ('id', 'name', 'description', 'org_type', 'status', 'date_add', 'client_options',)


class CompanyClientsFilters(django_filters.FilterSet):
    name_ac = django_filters.CharFilter(name="name", lookup_type='icontains')
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
    # request_freq = django_filters.NumberFilter(name="client_options__request_freq")

    class Meta:
        model = Companies
        fields = ['id', 'name', 'date_after', 'name_ac', 'status', 'org_type', 'client_options']