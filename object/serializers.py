# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import *
from company.serializers import CompanyClientsSerializer
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
    company = CompanyClientsSerializer(many=False, read_only=True)

    class Meta:
        model = Objects
        fields = ('pk', 'name', 'company', 'type', 'lat', 'lng', 'date_add', 'date_update',)


class ObjectsBunkerFlowSerializer(serializers.ModelSerializer):
    # type = ObjectTypesSerializer(many=False, read_only=True)
    company = CompanyClientsSerializer(many=False, read_only=True)

    class Meta:
        model = Objects
        fields = ('pk', 'name', 'company', 'type', )
