# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import CompanyOrgTypes
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from company.serializers import *


class UnitGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitGroups
        fields = ('pk', 'val', 'description')


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Persons
        fields = ('id', 'nick_name', 'given_name', 'family_name')


class ContactsSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False, required=False)
    # company = CompanyClientsSerializer(many=False, required=False)

    class Meta:
        model = Contacts
        # fields = ['id', 'role']
        fields = ['id', 'phonenumber', 'is_work', 'person', 'date_add']


class ContactsFilters(django_filters.FilterSet):

    class Meta:
        model = Contacts
        fields = ['id', 'phonenumber', 'is_work']


class EmplpoeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTypes
        fields = ('pk', 'val',)


class EmployeeRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRoles
        fields = ('pk', 'val',)


class EmployeeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeStatuses
        fields = ('pk', 'val',)


class EmployiesSerializer(serializers.ModelSerializer):
    type = EmplpoeeTypeSerializer(many=False, required=False)
    role = EmployeeRoleSerializer(many=False, required=False)
    person = PersonSerializer(many=False, required=False)
    status = EmployeeStatusSerializer(many=False, required=False)

    class Meta:
        model = Employies
        fields = ('pk', 'person', 'type', 'role', 'date_add', 'date_update', 'comment', 'status')


class EmployiesFilters(django_filters.FilterSet):
    # date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
    # request_freq = django_filters.NumberFilter(name="client_options__request_freq")

    class Meta:
        model = Employies
        fields = ['type', 'role', 'status']