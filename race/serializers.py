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


class RaceTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceTypes
        fields = ('pk', 'val',)


class RaceCargoTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceCargoTypes
        fields = ('pk', 'val',)


class RaceSerializer(serializers.ModelSerializer):
    # company = CompanyClientsSerializer(many=False, read_only=True, allow_null=False)
    # contragent = ContragentUlSerializer(many=False, read_only=True, allow_null=False)
    # car = CarsSerizlizer(many=False, read_only=True, allow_null=False)
    # driver = EmployiesSerializer(many=False, read_only=True, allow_null=False)
    # race_type = RaceTypesSerializer(many=False, read_only=True)
    # cargo_type = RaceCargoTypesSerializer(many=False, read_only=True)
    # object = ObjectsSerializer(many=False, read_only=True, allow_null=False)
    # bunker_type = BunkerTypesSerializer(many=False, read_only=True, allow_null=False)
    # dump = DumpsSerializer(many=False, read_only=True, allow_null=True, )
    driver = DriverSerializer(read_only=True)

    class Meta:
        model = Races
        depth = 1
        # nested_depth = 1
        fields = ('pk',
                  'company',
                  'contragent',
                  'object',
                  'car',
                  'driver',
                  'race_type',
                  'cargo_type',

                  'price',
                  'sum',
                  'pay_way',
                  'paid',
                  'hodkis',

                  'bunker_type',
                  'bunker_qty',

                  'dump',
                  'dump_pay_type',
                  'dump_cash',
                  'dump_cash_comment',
                  'dump_cash_extra',
                  'dump_comment',
                  'recommendation',
                  'date_race',
                  'date_add',
                  'mark_required',
                  'mark_done'
                  )


class RaceFilters(django_filters.FilterSet):
    driver_family_name_ac = django_filters.CharFilter(name="driver__person__family_name", lookup_type='icontains')
    car_name = django_filters.CharFilter(name="car__nick_name", lookup_type='icontains')
    company_name = django_filters.CharFilter(name="company__name", lookup_type='icontains')
    object_name = django_filters.CharFilter(name="object__name", lookup_type='icontains')
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_race", lookup_type='gte')
    date_before = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_race", lookup_type='lte')
    need_mark = django_filters.MethodFilter()

    def filter_need_mark(self, queryset, value):
        if not value:
            return queryset

        queryset = queryset.filter(mark_required=True, mark_done__isnull=True)
        return queryset

    class Meta:
        model = Races
        fields = [
            'car',
            'car__load_type',
            'salary_tarif',
            'driver',
            'date_race',
            'bunker_type',
            'pay_way',
        ]

