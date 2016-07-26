# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents
from django.db import transaction
from django.db.models import F


class SalaryFlow(models.Model):
    operation_types = ([0, 'начисление зарплаты за рейсы'], [1, 'начисление премии'], [2, 'начисление штрафа'], [3, 'выдача аванса'], [4, 'окончательный расчет'],)

    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey('person.Employies', null=False, blank=False)
    year = models.IntegerField(null=False, blank=False)
    month = models.IntegerField(null=False, blank=False)
    type = models.IntegerField(null=False, blank=False, choices=operation_types)
    sum = models.FloatField(null=False, blank=False)
    comment = models.CharField(max_length=255L, null=True, blank=True)

    class Meta:
        db_table = 'salary_flow'
        managed = False
        verbose_name_plural = 'Зарплата / Начисления'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.date_add, self.sum)