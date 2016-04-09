# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import *
from company.serializers import CompanyClientsSerializer, AddressSerializer
from person.models import Employies
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters


class ObjectTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectTypes
        fields = ('pk', 'val',)


class ObjectsSerializer(serializers.ModelSerializer):
    type = ObjectTypesSerializer(many=False, read_only=True)
    company = CompanyClientsSerializer(many=False, read_only=True, allow_null=True, required=False)
    address = AddressSerializer(many=False, read_only=True,  allow_null=True, required=False)

    class Meta:
        model = Objects
        # fields = ('pk', 'name', 'company', 'type', 'address', 'date_add', 'date_update',)
        fields = ('pk', 'name', 'company', 'type', 'address', 'date_add', 'date_update',)


class ObjectsBunkerFlowSerializer(serializers.ModelSerializer):
    # type = ObjectTypesSerializer(many=False, read_only=True)
    company = CompanyClientsSerializer(many=False, read_only=True)

    class Meta:
        model = Objects
        fields = ('pk', 'name', 'company', 'type', )


class ObjectFilters(django_filters.FilterSet):
    name_ac = django_filters.CharFilter(name="name", lookup_type='icontains')
    # date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
    # request_freq = django_filters.NumberFilter(name="client_options__request_freq")

    class Meta:
        model = Objects
        fields = ['name', 'name_ac', 'type', 'company__name', 'address__street', 'company' ]


class ObjectContactsSerializer(serializers.ModelSerializer):
    object = ObjectsSerializer(many=False, read_only=True)

    class Meta:
        model = ObjectContacts
        fields = ['company_contact', 'object']


class ObjectContactsFilters(django_filters.FilterSet):

    class Meta:
        model = ObjectContacts
        fields = ['object',]
