# -*- coding: utf8 -*

from django.db import models


class TalonsFlow(models.Model):
    operation_types = ([0, 'приобретение'], [1, 'свалка'], [2, 'передача'], [3, 'снятие'], [4, 'утилизация'],)
    employee_groups = ([0, 'офис'], [1, 'водители'])

    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    joined_operation = models.ForeignKey('self', null=True, blank=True)
    operation_type = models.IntegerField(null=False, blank=False, choices=operation_types)
    employee_group = models.IntegerField(null=False, blank=False, choices=employee_groups)
    dump_group = models.ForeignKey('dump.DumpGroups', null=False, blank=False, editable=True, related_name='talon_flow_operation')
    dds_operation = models.ForeignKey('dds.DdsFlow', null=True, blank=True, editable=True, related_name='dds_flow_operation')
    qty = models.IntegerField(null=False, blank=False)
    paid_qty = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    summ = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    paid_summ = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    employee = models.ForeignKey('person.Employies', null=True, blank=True, editable=True, related_name='dds_flow_operation')
    comment = models.CharField(max_length=255L, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'talons_flow'
        verbose_name_plural = 'Талоны / Движение талонов'

        def __unicode__(self):
            return u'[%s] %s' % (self.id, self.operation_type)
