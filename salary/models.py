# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents
from django.db import transaction, connection
from django.db.models import F
from django.db import transaction
from common.dbtools import fetch_sql_allintuple, fetch_sql_row

import logging
log = logging.getLogger('django')




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


class SalarySummaryManager(models.Manager):
    def get_queryset(self):
        return super(SalarySummaryManager, self).get_queryset().select_related('employee')

    @staticmethod
    def driver_month_stats(date_start, date_end, driver_pk):
        result = {}
        query = """SELECT
                      T.car_id
                      ,C.reg_num
                      ,C.nick_name
                      ,C.fuel_norm
                      ,T2.first_km
                      ,T2.last_km
                      ,T2.total_run
                      ,T2.last_lit
                      ,T2.total_races
                      ,T2.total_hodkis
                      ,SUM(lit) - T2.last_lit AS total_lit
                      ,ROUND((T2.total_run / T2.total_hodkis),1) AS km_on_hodkis
                      ,ROUND((((SUM(lit) - T2.last_lit) / T2.total_run) * 100),1) AS lit_on_100
                      ,ROUND((((SUM(lit) - T2.last_lit) / T2.total_run) * 100),1) - C.fuel_norm AS fuel_overuse
                    FROM refuels2 AS T
                    LEFT JOIN cars AS C ON C.id = T.car_id
                    LEFT JOIN ( SELECT
                                            R.car_id
                                            ,R.lit AS last_lit
                                            ,G1.first_km
                                            ,G1.last_km
                                            ,(G1.last_km - G1.first_km) AS total_run
                                            ,Z.total_races
                                            ,Z.total_hodkis
                                        FROM refuels2 AS R
                                        LEFT JOIN ( SELECT
                                                                car_id,
                                                                IFNULL( ( SELECT MAX(KM)
                                                                            FROM refuels2 AS R2
                                                                            WHERE date < %(date_start)s
                                                                            AND R2.car_id = R1.car_id
                                                                        ),
                                                                    MIN(KM) ) AS first_km
                                                                    ,MAX(km) as last_km
                                                                FROM refuels2 AS R1
                                                                WHERE
                                                                    date > %(date_start)s
                                                                    AND date < %(date_end)s
                                                                GROUP BY car_id
                                            ) AS G1 ON G1.car_id = R.car_id
                                        LEFT JOIN (
                                                SELECT
                                                    car_id
                                                    ,COUNT(id) AS total_races
                                                    ,COUNT(hodkis) AS total_hodkis
                                                FROM races
                                                WHERE date_race BETWEEN %(date_start)s AND %(date_end)s
                                                GROUP BY car_id
                                        ) AS Z ON Z.car_id = R.car_id
                                WHERE R.km = G1.last_km
                                GROUP BY car_id
                                ) AS T2 ON T2.car_id = T.car_id
                    WHERE
                        T.km BETWEEN T2.first_km AND T2.last_km
                        AND T.driver_id = %(driver_pk)s
                    GROUP BY car_id"""
        limit = 10
        params = {'date_start': date_start, 'date_end': date_end, 'driver_pk': driver_pk}
        # cursor = connection.cursor()
        # cursor.execute(query, params)
        # for row in cursor.fetchall():
        #     log.info("== row: " % row)
        result['data'] = fetch_sql_allintuple(query, params=params)
        # try:
        #     result['data'] = fetch_sql_allintuple(query, params=params)
        # except TypeError as err:
        #         result['error'] = "Нет данных для отчета за указанный период"
        return result


class SalaryMonthSummary(models.Model):
    check_status_choices = ([0, 'анализ'], [1, 'контроль офис'], [2, 'контроль руководитель'], [3, 'выдача'], [4, 'закрыт'],)

    objects = SalarySummaryManager()

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
