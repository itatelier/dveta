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


class SalaryMonthSummary(models.Model):
    check_status_choices = ([0, 'анализ'], [1, 'контроль офис'], [2, 'контроль руководитель'], [3, 'выдача'], [4, 'закрыт'],)

    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField(null=False, blank=False)
    month = models.IntegerField(null=False, blank=False)
    employee = models.ForeignKey('person.Employies', null=False, blank=False)

    races_done = models.IntegerField(null=False, blank=False)
    hodkies = models.IntegerField(null=False, blank=False)
    run_km = models.IntegerField(null=False, blank=False)
    average_consumption = models.IntegerField(null=False, blank=False)

    over_run_status = models.NullBooleanField(null=True, blank=True, default=False)
    over_fuel_status = models.NullBooleanField(null=True, blank=True, default=False)
    mech_comment = models.CharField(max_length=255L, null=True, blank=True)

    over_run_penalty = models.FloatField(null=True, blank=True)
    over_fuel_penalty = models.FloatField(null=True, blank=True)
    misc_penalty = models.FloatField(null=True, blank=True)

    bonus_amount = models.FloatField(null=True, blank=True)
    deductions_amount = models.FloatField(null=True, blank=True)
    races_salary = models.FloatField(null=True, blank=True)
    compensation_amount = models.FloatField(null=True, blank=True)

    summary_salary_amount = models.FloatField(null=True, blank=True)
    paid_sum = models.FloatField(null=True, blank=True)
    remain_sum = models.FloatField(null=True, blank=True)
    check_status = models.NullBooleanField(null=True, blank=True, default=False, choices=check_status_choices)
    comment = models.CharField(max_length=255L, null=True, blank=True)

    class Meta:
        db_table = 'salary_month_summary'
        managed = False
        verbose_name_plural = 'Зарплата / Итоги месяца'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.date_add, self.sum)
