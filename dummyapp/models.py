# -*- coding: utf8 -*

from company.models import *
from django.db import models
from common.dbtools import fetch_sql_allintuple, fetch_sql_row


class DummyCompanies(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    www = models.CharField(max_length=255, blank=True)
    org_type = models.ForeignKey('company.CompanyOrgTypes', null=False, blank=False, related_name="org_type")
    rel_type = models.ForeignKey('company.CompanyRelTypes', null=False, blank=False)
    status = models.ForeignKey('company.CompanyStatus', null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dummy_companies'
        verbose_name_plural = 'Тестирование / Компании'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DummyFlowTrans(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dummy_transactions'
        verbose_name_plural = 'Тестирование / Бункеры транзацкции'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.date)


class BunkerFlowManager(models.Manager):
    @staticmethod
    def get_flow():
        query = """SELECT * FROM dummy_flow"""
        result = fetch_sql_allintuple(query, params=None)
        return result


class DummyFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    transaction = models.ForeignKey('DummyFlowTrans', null=False, blank=False)
    object = models.ForeignKey('object.Objects', null=False, blank=False)
    qty = models.IntegerField()
    objects = BunkerFlowManager()
    # selfrelated = models.ForeignKey('self', to_field='transaction',  default=None, null=True)

    class Meta:
        db_table = 'dummy_flow_clear'
        verbose_name_plural = 'Тестирование / Бункеры поток'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.transaction)