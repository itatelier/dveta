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
from rest_framework import viewsets, generics, filters
import django_filters


class RaceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceTypes
        fields = ('pk', 'val',)


class RaceCargoTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceCargoTypes
        fields = ('pk', 'val',)


class RaceSerializer(serializers.ModelSerializer):
    company = CompanyClientsSerializer(many=False, read_only=True, allow_null=False)
    contragent = ContragentUlSerializer(many=False, read_only=True, allow_null=False)
    car = CarsSerizlizer(many=False, read_only=True, allow_null=False)
    driver = EmployiesSerializer(many=False, read_only=True, allow_null=False)
    race_type = RaceTypesSerializer(many=False, read_only=True)
    race_cargo_type = RaceCargoTypesSerializer(many=False, read_only=True)
    object = ObjectsSerializer(many=False, read_only=True, allow_null=False)
    bunker_type = BunkerTypesSerializer(many=False, read_only=True, allow_null=False)
    dump = DumpsSerializer(many=False, read_only=True, allow_null=True, )

    class Meta:
        model = Races
        depth = 1
        nested_depth = 1
        fields = ('pk',
                  'company',
                  'contragent',
                  'object',
                  'car',
                  'driver',
                  'race_type',
                  'race_cargo_type',

                  'price',
                  'summ',
                  'pay_way',
                  'paid',

                  'bunker_type',
                  'bunker_qty',

                  'dump',
                  'dump_pay_type',
                  'dump_cash',
                  'dump_cash_comment',
                  'dump_comment',
                  'recommendation',
                  'date_race',
                  'date_add',
                  )


class RaceFilters(django_filters.FilterSet):
    # name_ac = django_filters.CharFilter(name="name", lookup_type='icontains')
    # date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')
    # request_freq = django_filters.NumberFilter(name="client_options__request_freq")

    class Meta:
        model = Races
        fields = [
            'company',
            'contragent',
            'object',
            'car',
            'driver',
        ]

