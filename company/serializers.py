# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import *
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from person.serializers import ContactsSerializer


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
        fields = ('pk', 'request_tickets', 'request_special_sign', 'request_freq', 'use_client_talons_only', 'pay_condition', 'pay_type', 'pay_form', 'credit_limit')


class CompanyClientsSerializer(serializers.ModelSerializer):
    org_type = OrgTypeSerializer(many=False, required=False)
    status = StatusSerializer(many=False, required=False)
    client_options = ClientOptionsSerializer(many=False, required=False)

    class Meta:
        model = Companies
        fields = ('id', 'name', 'description', 'comment', 'org_type', 'status', 'date_add', 'client_options')


class CompanyClientsFilters(django_filters.FilterSet):
    name_ac = django_filters.CharFilter(name="name", lookup_type='icontains')
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
    # request_freq = django_filters.NumberFilter(name="client_options__request_freq")

    class Meta:
        model = Companies
        fields = ['id', 'name', 'date_after', 'name_ac', 'status', 'org_type', 'client_options__request_freq', 'client_options__pay_condition', 'client_options__pay_type', 'client_options__pay_form']


class CompanyContactsSerializer(serializers.ModelSerializer):
    company = CompanyClientsSerializer(many=False, read_only=True)
    contact = ContactsSerializer(many=False,  read_only=True)

    class Meta:
        model = CompanyContacts
        depth = 3
        fields = ['id', 'company', 'contact', 'show_in_card']


class CompanyContactsSerializerShort(CompanyContactsSerializer):
    company = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = CompanyContacts
        depth = 3
        fields = ['id', 'company', 'contact', 'show_in_card']


class CompanyContactsFilters(django_filters.FilterSet):
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="contact__date_add", lookup_type='gte')

    class Meta:
        model = CompanyContacts
        fields = ['id', 'contact__phonenumber', 'contact__is_work', 'contact__date_add', 'company__name', 'company__org_type', 'company__status' ]