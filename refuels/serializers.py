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
from dump.serializers import *

from person.models import Employies
from rest_framework import serializers
from rest_framework import viewsets, generics, filters, fields
import django_filters


class FuelCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelCompanies
        fields = ('pk', 'name',)


class FuelCardsSerializer(serializers.ModelSerializer):
    fuel_company = FuelCompanySerializer(many=False, read_only=True, allow_null=False)

    class Meta:
        model = FuelCards
        fields = ('pk', 'fuel_company', 'num', 'assigned_car')


class RefuelsFlowSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(many=False, read_only=True, allow_null=False)
    car = CarsSimpleSerializer(many=False, read_only=True, allow_null=False)
    fuel_card = FuelCardsSerializer(many=False, read_only=True, allow_null=True)

    class Meta:
        depth = 1
        model = RefuelsFlow
        fields = ('pk', 'driver', 'car', 'date', 'type', 'fuel_card', 'amount', 'summ', 'km', 'comment', 'checked')


class RefuelsFlowFilters(django_filters.FilterSet):
    driver_family_name_ac = django_filters.CharFilter(name="driver__person__family_name", lookup_type='icontains')
    car_name = django_filters.CharFilter(name="car__nick_name", lookup_type='icontains')
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_race", lookup_type='gte')
    date_before = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_race", lookup_type='lte')

    class Meta:
        model = RefuelsFlow
        fields = [
            'driver_family_name_ac',
            'car_name',
            'date_after',
            'date_before',
            'type',
            'fuel_card',
            'checked',
        ]
