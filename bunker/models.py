# -*- coding: utf8 -*

from django.db import models
from common.dbtools import fetch_sql_allintuple, fetch_sql_row


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
    @staticmethod
    def by_object_id(object_id):
        query = """SELECT
                    SUM(
                        CASE
                            WHEN object_out_id = %s THEN qty * (-1)
                            WHEN object_in_id = %s THEN qty
                            ELSE 0
                        END
                        ) AS summ
                    FROM bunker_flow"""
        params = (object_id, object_id, )
        result = fetch_sql_row(query, params)
        return result[0]

    @staticmethod
    def by_object_type():
        query = """SELECT t.val as type_name, type_id, SUM(qty) AS summ
                    FROM (
                            SELECT
                                    o.type_id as type_id
                                    ,object_out_id as object_id
                                    ,-1 * qty as qty
                          FROM bunker_flow AS f1
                            LEFT JOIN objects AS o ON o.id = object_out_id
                            UNION ALL
                            SELECT
                                    o.type_id as type_id
                                    ,object_in_id as object_id
                                    ,qty
                          FROM bunker_flow AS f1
                            LEFT JOIN objects AS o ON o.id = object_in_id
                    ) AS flow
                    LEFT JOIN object_types as t ON t.id = type_id
                    WHERE type_id != 'Null'
                    GROUP BY type_id"""
        result = fetch_sql_allintuple(query, params=None)
        return result

    @staticmethod
    def by_company_status():
        query = """SELECT s1.val as status_name, company_status_id, SUM(qty) as summ
                    FROM (
                    SELECT
                        f1.qty as qty
                            ,f1.object_in_id as object_id
                        ,o1.type_id as object_type_id
                            ,c1.status_id as company_status_id
                    FROM bunker_flow AS f1
                    LEFT JOIN objects AS o1 ON f1.object_in_id = o1.id
                    LEFT JOIN companies AS c1 on o1.company_id = c1.id
                    WHERE o1.type_id = 3
                    UNION ALL
                    SELECT
                        -1* f1.qty as qty
                            ,f1.object_out_id as object_id
                        ,o1.type_id as object_type_id
                            ,c1.status_id as company_status_id
                    FROM bunker_flow AS f1
                    LEFT JOIN objects AS o1 ON f1.object_out_id = o1.id
                    LEFT JOIN companies AS c1 on o1.company_id = c1.id
                    WHERE o1.type_id = 3
                    ) as flow
                    LEFT JOIN company_status AS s1 ON company_status_id = s1.id
                    GROUP BY company_status_id"""
        result = fetch_sql_allintuple(query, params=None)
        return result


class BunkerAllDefaultManager(models.Manager):
    def get_queryset(self):
        return super(BunkerAllDefaultManager, self).get_queryset().select_related('bunker_type', 'operation_type', 'object_in', 'object_out')


class BunkerFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    object_in = models.ForeignKey('object.Objects', null=True, blank=True, editable=True, related_name="object_in")
    # object_in_type = models.ForeignKey('object.ObjectTypes', null=False, blank=False, editable=True, related_name="object_in_type")
    object_out = models.ForeignKey('object.Objects', null=True, blank=True, editable=True, related_name="object_out")
    # object_out_type = models.ForeignKey('object.ObjectTypes', null=False, blank=False, editable=True, related_name="object_out_type")
    qty = models.IntegerField(null=False, blank=False, editable=True)
    bunker_type = models.ForeignKey('bunker.BunkerTypes', null=False, blank=False, editable=True)
    operation_type = models.ForeignKey('bunker.BunkerOperationTypes', null=False, blank=False, editable=True)
    remains = BunkerRemainsManager()
    objects = BunkerAllDefaultManager()

    class Meta:
        db_table = 'bunker_flow'
        verbose_name_plural = 'Бункеры / Движение'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.date, self.qty)


