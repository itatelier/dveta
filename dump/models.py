# -*- coding: utf8 -*

from django.db import models
from django.db import connection

import logging
log = logging.getLogger('django')

class DumpGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'dump_groups'
        verbose_name_plural = 'Полигоны / Группы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class Dumps(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    group = models.ForeignKey('DumpGroups', null=False, blank=False, editable=True, related_name='dumps')
    name = models.CharField(max_length=200L, null=False, blank=False)
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
        row = cursor.fetchone()
        # log.info("--- Proc result: %s Row count: %s" % (row[0], row[1]))
        cursor.close()
        return row[0], row[1]


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
    comment = models.CharField(max_length=255L, null=True, blank=True)

    objects = TalonsFlowManager()

    class Meta:
        db_table = 'talons_flow'
        verbose_name_plural = 'Талоны / Движение талонов'

        def __unicode__(self):
            return u'[%s] %s' % (self.id, self.operation_type)

