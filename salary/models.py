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
    def drivers_list_races_and_summary(date_start, date_end):
        result = {}
        query = """SELECT
                    R2.driver_id
                    ,R2.races_done as races
                    ,R2.driver_family_name
                    ,R2.driver_given_name
                    ,R2.driver_nick_name
                    ,ss.id as summary_id
                	,ss.check_status
                    ,ss.date_add
                    ,ss.races_done
                    ,ss.total_hodkis
                    ,ss.total_run
                    ,ss.average_consumption
                    ,ss.over_run_status
                    ,ss.over_fuel_status
                    ,ss.mech_comment
                    ,ss.over_run_penalty
                    ,ss.over_fuel_penalty
                FROM (
                        SELECT
                            R.driver_id AS driver_id
                            ,P.id
                            ,P.nick_name AS driver_nick_name
                            ,P.family_name AS driver_family_name
                            ,P.given_name AS driver_given_name
                            ,COUNT(R.id) AS races_done
                        FROM races AS R
                        JOIN employies AS E ON E.id = R.driver_id
                        JOIN persons AS P ON P.id = E.person_id
                        WHERE (R.date_race >= %(date_start)s AND R.date_race < %(date_end)s)
                        GROUP BY driver_id
                        ) AS R2
                LEFT OUTER JOIN salary_month_summary AS ss ON ss.employee_id = R2.driver_id
                	AND `ss`.`month` = MONTH(%(date_start)s)
                    AND `ss`.`year`= YEAR(%(date_start)s)"""
        params = {'date_start': date_start, 'date_end': date_end}
        result['data'] = fetch_sql_allintuple(query, params=params)
        return result

    @staticmethod
    def driver_month_stats(date_start, date_end, driver_pk):
        query = """SELECT 
                    RR.car_id
                    ,C.reg_num
                    ,C.nick_name
                    ,C.fuel_norm
                    ,COUNT(*) AS races_done
                    ,SUM(RR.hodkis) AS total_hodkis
                    ,IFNULL(J3.total_refuels,0) AS total_refuels
                    ,J3.total_amount
                    ,J3.total_run
                    ,ROUND(((J3.total_amount / J3.total_run) * 100),1) AS lit_on_100
                    ,ROUND(J3.total_run / SUM(RR.hodkis), 1) AS km_on_hodkis
                    ,(ROUND(((J3.total_amount / J3.total_run) * 100),1)) - C.fuel_norm AS fuel_overuse
                FROM races AS RR
                LEFT JOIN cars AS C ON C.id = RR.car_id
                LEFT OUTER JOIN (
                                                SELECT
                                                        R2.car_id
                                                        ,COUNT(*) AS total_refuels
                                                        ,(SUM(R2.amount) - J2.last_refuel_amount) AS total_amount
                                                        ,J2.total_run
                                                FROM refuels_flow AS R2
                                                LEFT OUTER JOIN (
                                                                                SELECT
                                                                                    R.car_id
                                                                                    ,R.amount AS last_refuel_amount
                                                                                    ,G1.first_km
                                                                                    ,G1.last_km
                                                                                    ,(G1.last_km - G1.first_km) AS total_run
                                                                                FROM refuels_flow AS R
                                                                                LEFT JOIN ( SELECT 
                                                                                                        car_id,
                                                                                                        IFNULL( ( SELECT MAX(KM) 
                                                                                                                    FROM refuels_flow AS R2
                                                                                                                    WHERE date_refuel < %(date_start)s 
                                                                                                                    AND R2.car_id = R1.car_id
                                                                                                                    AND R2.driver_id = %(driver_pk)s
                                                                                                                ),
                                                                                                            MIN(KM) ) AS first_km
                                                                                                            ,MAX(km) as last_km
                                                                                                        FROM refuels_flow AS R1
                                                                                                        WHERE date_refuel >= %(date_start)s AND date_refuel < %(date_end)s
                                                                                                        AND driver_id = %(driver_pk)s
                                                                                                        GROUP BY car_id
                                                                                ) AS G1 ON G1.car_id = R.car_id
                                                                                WHERE R.km = G1.last_km	
                                                                                
                                                ) AS J2 ON J2.car_id = R2.car_id
                                                WHERE	R2.km BETWEEN J2.first_km AND J2.last_km
                                                AND R2.driver_id = %(driver_pk)s
                                                GROUP BY car_id
                ) AS J3 ON J3.car_id = RR.car_id
                WHERE RR.date_race >= %(date_start)s AND RR.date_race < %(date_end)s
                
                GROUP BY car_id"""
        params = {'date_start': date_start, 'date_end': date_end, 'driver_pk': driver_pk}
        result = fetch_sql_allintuple(query, params=params)
        return result

    @staticmethod
    def refuels_on_period_for_car(date_start, date_end, car_pk):
        #    получаем список всех заправок от (последней ПЕРЕД периодом или первой ВНУТРИ периода) до последней ВНУТРИ
        #    периода. Cписок для расчета "пробега" и показа в отчете по всем заправкам за период
        #    БЕЗ УЧЕТА ДРАЙВЕРА, для КОНКРЕТНОЙ машины
        query = """SELECT
                        R2.car_id
                        ,R2.date_refuel
                        ,R2.driver_id
                        ,P.id AS driver_person_id
                        ,P.family_name
                        ,P.given_name
                        ,P.nick_name
                        ,R2.amount
                        ,R2.km
                        ,R2.sum
                        ,R2.checked
                FROM refuels_flow AS R2
                LEFT JOIN employies AS E ON E.id = R2.driver_id
                LEFT JOIN persons AS P ON P.id = E.person_id
                LEFT OUTER JOIN (
                        SELECT
                        car_id,
                        IFNULL( ( SELECT MAX(KM)
                                    FROM refuels_flow AS R2
                                    WHERE date_refuel < %(date_start)s
                                        AND R2.car_id = R1.car_id
                                        AND R2.car_id = %(car_pk)s
                                ),
                            MIN(KM) ) AS first_km
                            ,MAX(km) as last_km
                        FROM refuels_flow AS R1
                        WHERE date_refuel >= %(date_start)s AND date_refuel < %(date_end)s
                        AND R1.car_id = %(car_pk)s
                        GROUP BY car_id
                ) AS J2 ON J2.car_id = R2.car_id
                WHERE	R2.km BETWEEN J2.first_km AND J2.last_km"""
        params = {'date_start': date_start, 'date_end': date_end, 'car_pk': car_pk}
        result = fetch_sql_allintuple(query, params=params)
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
    total_hodkis = models.DecimalField(decimal_places=1, max_digits=4, null=False, blank=False)
    km_on_hodkis = models.DecimalField(decimal_places=1, max_digits=4, null=False, blank=False)
    total_run = models.IntegerField(null=False, blank=False)
    total_amount = models.IntegerField(null=False, blank=False)
    average_consumption = models.DecimalField(decimal_places=1, max_digits=4, null=False, blank=False)

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
    check_status = models.IntegerField(null=True, blank=True, default=False, choices=check_status_choices)
    comment = models.CharField(max_length=255L, null=True, blank=True)

    class Meta:
        db_table = 'salary_month_summary'
        managed = False
        verbose_name_plural = 'Зарплата / Итоги месяца'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.date_add)
