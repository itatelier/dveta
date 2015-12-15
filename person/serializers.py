# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import CompanyOrgTypes
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from company.serializers import *


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Persons
        fields = ('id', 'nick_name', 'given_name', 'family_name')


class ContactsFilters(django_filters.FilterSet):
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
    # request_freq = django_filters.NumberFilter(name="client_options__request_freq")

    class Meta:
        model = Contacts
        fields = ['id', 'role', 'email', 'phonenumber', 'comment', 'is_work', 'date_add']


class ContactsSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False, required=False)
    company = CompanyClientsSerializer(many=False, required=False)

    class Meta:
        model = Contacts
        # fields = ['id', 'role']
        fields = ['id', 'role', 'email', 'phonenumber', 'comment', 'is_work', 'person', 'company', 'date_add']
