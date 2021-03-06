# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import *
from person.models import Employies
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters
from person.serializers import EmployiesSerializer, UnitGroupsSerializer, DriverSerializer


class CarBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrands
        fields = ('pk', 'val',)


class CarModelsSerializer(serializers.ModelSerializer):
    brand = CarBrandsSerializer(many=False, read_only=True)

    class Meta:
        model = CarModels
        fields = ('pk', 'val', 'brand')


class CarFuelTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarFuelTypes
        fields = ('pk', 'val',)


class CarStatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarStatuses
        fields = ('pk', 'val',)


class CarsSerizlizer(serializers.ModelSerializer):
    model = CarModelsSerializer(many=False, read_only=True)
    fuel_type = CarFuelTypesSerializer(many=False, read_only=True)
    mechanic = DriverSerializer(many=False, read_only=True)
    unit_group = UnitGroupsSerializer(many=False, read_only=True)
    status = CarStatusesSerializer(many=False, read_only=True)
    driver = DriverSerializer(allow_null=True)

    class Meta:
        depth = 1
        model = Cars
        fields = ('pk', 'model', 'fuel_type', 'load_type', 'unit_group', 'reg_num', 'nick_name', 'comment', 'trailer_attached', 'date_add', 'status', 'driver', 'mechanic')


class CarsSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Cars
        fields = ('pk', 'reg_num', 'nick_name', 'comment', 'trailer_attached', 'date_add', )


class CarFilters(django_filters.FilterSet):
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')

    class Meta:
        model = Cars
        fields = ['model', 'fuel_type', 'mechanic', 'unit_group', 'status', 'driver', 'comment']
