# -*- coding: utf8 -*

from django.contrib.auth.models import User, Group
from models import *
from company.models import CompanyOrgTypes
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class OrgTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyOrgTypes
        fields = ('pk', 'val',)


class CompanySerializer(serializers.ModelSerializer):
    # pk = serializers.IntegerField(read_only=True)
    # name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    # description = serializers.CharField(required=False, allow_blank=True, max_length=255)
    # www = serializers.CharField(required=False, allow_blank=True, max_length=250)
    org_type = OrgTypeSerializer(many=False, required=False)
    # rel_type = serializers.BooleanField(required=True)
    # date_add = serializers.DateTimeField(required=True)

    class Meta:
        model = DummyCompanies
        fields = ('url', 'id', 'name', 'description', 'www', 'org_type', 'rel_type', 'status', 'date_add',)