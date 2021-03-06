# -*- coding: utf8 -*

from django.db import models
from django.db import connection
from common.dbtools import fetch_sql_allintuple, fetch_sql_row


import logging
log = logging.getLogger('django')

class DumpGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = 'dump_groups'
        verbose_name_plural = 'Полигоны / Группы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class Dumps(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    group = models.ForeignKey('DumpGroups', null=False, blank=False, editable=True, related_name='dumps')
    name = models.CharField(max_length=200, null=False, blank=False)
    pay_type = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'dumps'
        verbose_name_plural = 'Полигоны'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class TalonsFlowManager(models.Manager):
    def get_queryset(self):
        return super(TalonsFlowManager, self).get_queryset().select_related('employee', 'dump_group', )

    @staticmethod
    def move_between_proc(operation_type, dump_group_id, qty, employee_out_id, employee_in_id, employee_group_out_id, employee_group_in_id):
        cursor = connection.cursor()
        ret = cursor.callproc("talons_move", (operation_type, dump_group_id, qty, employee_out_id, employee_in_id, employee_group_out_id, employee_group_in_id))
        log.info("--- Proc params: operation_type=%s dump_group_id=%s qty=%s employee_out_id=%s employee_in_id=%s employee_group_out_id=%s employee_group_in_id=%s" % (operation_type, dump_group_id, qty, employee_out_id, employee_in_id, employee_group_out_id, employee_group_in_id))
        row = cursor.fetchone()
        #log.info("--- Proc result: %s Row count: %s" % (row[0], row[1]))
        cursor.close()
        return row[0], row[1]

    @staticmethod
    def report_by_dump_group():
        query = """SELECT
                    dump_groups.name as dump_group_name
                    ,flow.dump_group_id,
                    SUM(IF(flow.employee_group = 0, IFNULL(remains, qty) , NULL)) AS remains0,
                    SUM(IF(flow.employee_group = 1, IFNULL(remains,qty) , NULL)) AS remains1
                FROM talons_flow as flow
                JOIN dump_groups AS dump_groups ON flow.dump_group_id = dump_groups.id
                WHERE (is_closed IS NULL
                    AND NOT (operation_type IN (1, 2)))
                GROUP BY dump_group_id"""
        result = fetch_sql_allintuple(query, params=None)
        return result


class TalonsFlow(models.Model):
    operation_types = ([0, 'приобретение'], [1, 'расход'], [2, 'снятие'], [3, 'передача'], [4, 'утилизация'],)
    employee_groups = ([0, 'офис'], [1, 'водители'])

    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    operation_type = models.IntegerField(null=False, blank=False, choices=operation_types)
    employee = models.ForeignKey('person.Employies', null=True, blank=True, editable=True, related_name='dds_flow_operation')
    employee_group = models.IntegerField(null=False, blank=False, choices=employee_groups)
    dump_group = models.ForeignKey('dump.DumpGroups', null=False, blank=False, editable=True, related_name='talon_flow_operation')
    dds_operation = models.ForeignKey('dds.DdsFlow', null=True, blank=True, editable=True, related_name='dds_flow_operation')
    qty = models.IntegerField(null=False, blank=False)
    paid_qty = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    sum = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    paid_sum = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    remains = models.IntegerField(null=True, blank=True)
    is_closed = models.NullBooleanField(null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)

    objects = TalonsFlowManager()

    class Meta:
        db_table = 'talons_flow'
        verbose_name_plural = 'Талоны / Движение талонов'

        def __unicode__(self):
            return u'[%s] %s' % (self.id, self.operation_type)

