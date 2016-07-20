# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import *
from contragent.models import *
from company.serializers import *
from contragent.serializers import *
from car.serializers import *
from person.serializers import *
from object.serializers import *
from bunker.serializers import *
from person.serializers import EmployiesSerializer, UnitGroupsSerializer, EmployeeSerializerShort



from person.models import Employies
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters


class DumpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dumps
        fields = ('pk', 'name',)


class DumpGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DumpGroups
        fields = ('pk', 'name',)


class TalonsOperationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TalonsFlow
        depth = 1
        fields = ('pk', 'date', 'operation_type', 'employee', 'employee_group', 'dump_group', 'dds_operation', 'qty', 'price', 'sum', 'comment', )


class TalonsFlowSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializerShort(many=False, read_only=True)
    employee_group = serializers.SerializerMethodField()
    operation_type = serializers.SerializerMethodField()

    class Meta:
        model = TalonsFlow
        depth = 1
        fields = ('pk', 'date', 'operation_type', 'employee', 'employee_group', 'dump_group', 'dds_operation', 'qty', 'price', 'sum', 'remains', 'is_closed', 'comment', )

    def get_employee_group(self, obj):
        return obj.get_employee_group_display()

    def get_operation_type(self, obj):
        return obj.get_operation_type_display()


class TalonsFlowFilters(django_filters.FilterSet):
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date", lookup_type='gte')
    date_before = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date", lookup_type='lte')
    not_closed = django_filters.BooleanFilter(name='is_closed', lookup_type='isnull')

    class Meta:
        model = TalonsFlow
        fields = ['date_after', 'date_before', 'operation_type', 'employee', 'employee_group', 'dump_group', 'not_closed']