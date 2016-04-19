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


from person.models import Employies
from rest_framework import serializers
from rest_framework import viewsets, generics, filters
import django_filters

class DumpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dumps
        fields = ('pk', 'name',)


