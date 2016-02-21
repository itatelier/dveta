# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import *
from person.models import Employies
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from object.serializers import ObjectsSerializer, ObjectsBunkerFlowSerializer
from common.rest_tools import action_at_evening
import logging
log = logging.getLogger('django')


class BunkerTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BunkerTypes
        fields = ('pk', 'val',)


class BunkerOperationTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = BunkerOperationTypes
        fields = ('pk', 'val', )


class BunkerFlowSerializer(serializers.ModelSerializer):
    bunker_type = BunkerTypesSerializer(many=False, read_only=True)
    operation_type = BunkerOperationTypesSerializer(many=False, read_only=True)
    # object_in = serializers.PrimaryKeyRelatedField(many=False, read_only=True, allow_null=True)
    # object_out = serializers.PrimaryKeyRelatedField(many=False, read_only=True, allow_null=True)
    object_in = ObjectsBunkerFlowSerializer(many=False, read_only=True, allow_null=True)
    object_out = ObjectsBunkerFlowSerializer(many=False, read_only=True, allow_null=True)

    class Meta:
        model = BunkerFlow
        # fields = ('pk', 'date', 'bunker_type', 'operation_type', 'object_in', 'object_in__type', 'object_out', 'object_out__type', 'qty', )
        fields = ('pk', 'date', 'bunker_type', 'operation_type', 'object_in', 'object_out', 'qty', )


class BunkerFlowFilters(django_filters.FilterSet):
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date", lookup_type='gte')
    date_before = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date", lookup_type='lte', action=action_at_evening)

    class Meta:
        model = BunkerFlow
        fields = ['bunker_type', 'operation_type', 'date_after', 'date_before']



