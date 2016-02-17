# -*- coding: utf8 -*

from django.db import models
from common.dbtools import fetch_sql_allintuple


class BunkerTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'bunker_types'
        verbose_name_plural = 'Бункеры / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class BunkerOperationTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'bunker_operation_types'
        verbose_name_plural = 'Бункеры / Типы операций'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class BunkerRemainsManager(models.Manager):

    def by_object_type(self):
        query = """SELECT object_id, SUM(qty) AS sum_qty
            FROM (
            SELECT
                object_out_id as object_id ,-1 * qty as qty
                FROM bunker_flow AS flow1
            UNION ALL
            SELECT
                object_in_id as object_id ,qty
                FROM bunker_flow
            ) AS flow
            GROUP BY object_id"""
        remains = fetch_sql_allintuple(query)
        return remains


class BunkerFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    object_in = models.ForeignKey('object.Objects', null=False, blank=False, editable=True, related_name="object_in")
    object_in_type = models.ForeignKey('object.ObjectTypes', null=False, blank=False, editable=True, related_name="object_in_type")
    object_out = models.ForeignKey('object.Objects', null=False, blank=False, editable=True, related_name="object_out")
    object_out_type = models.ForeignKey('object.ObjectTypes', null=False, blank=False, editable=True, related_name="object_out_type")
    qty = models.IntegerField(null=False, blank=False, editable=True)
    bunker_type = models.ForeignKey('bunker.BunkerTypes', null=False, blank=False, editable=True)
    operation_type = models.ForeignKey('bunker.BunkerOperationTypes', null=False, blank=False, editable=True)
    remains = BunkerRemainsManager()

    class Meta:
        db_table = 'bunker_flow'
        verbose_name_plural = 'Бункеры / Движение'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.date, self.qty)


