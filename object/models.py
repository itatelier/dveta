# -*- coding: utf8 -*

from django.db import models
from common.dbtools import fetch_sql_allintuple, fetch_sql_row



class ObjectTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'object_types'
        verbose_name_plural = 'Объекты / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class ObjectsManagerPlus(models.Manager):
    @staticmethod
    def list_bunker_remains(company_id):
        query = """SELECT
                        ob.id,
                        ob.name,
                        addresses.city,
                        addresses.street,
                        addresses.app,
                        addresses.lat,
                        addresses.lng,
                        gb.summ
                    FROM objects AS ob
                    LEFT JOIN
                            (
                            SELECT object_id, SUM(qty) as summ
                            FROM (
                                    SELECT
                                            f1.object_in_id as object_id
                                            ,f1.qty as qty
                                            ,o1.type_id as object_type_id
                                    FROM bunker_flow AS f1
                                    LEFT JOIN objects AS o1 ON f1.object_in_id = o1.id
                                    WHERE o1.type_id = 3
                                    UNION ALL
                                    SELECT
                                            f1.object_out_id as object_id
                                            ,-1* f1.qty as qty
                                            ,o1.type_id as object_type_id
                                    FROM bunker_flow AS f1
                                    LEFT JOIN objects AS o1 ON f1.object_out_id = o1.id
                                    WHERE o1.type_id = 3
                            ) as flow
                            GROUP BY object_id
                    ) as gb ON gb.object_id = ob.id
                    LEFT JOIN addresses on addresses.id = ob.address_id
                    WHERE ob.company_id = %s
                    ORDER BY summ DESC"""
        params = (company_id,)
        result = fetch_sql_allintuple(query, params)
        return result


class Objects(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=200L, null=False, blank=False)
    type = models.ForeignKey('ObjectTypes', null=False, blank=False, editable=True)
    company = models.ForeignKey('company.Companies', null=False, blank=False, editable=True)
    address = models.ForeignKey('company.Addresses', null=False, blank=False, editable=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    objects = ObjectsManagerPlus()

    class Meta:
        db_table = 'objects'
        verbose_name_plural = 'Объекты'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)
