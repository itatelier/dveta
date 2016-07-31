# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents
from django.db import transaction
from common.dbtools import fetch_sql_allintuple, fetch_sql_row
from django.db import connection

from django.db.models import F


class FuelCompanies(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'fuel_companies'
        managed = False
        verbose_name_plural = 'Заправки / Топливные компании'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class FuelTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255L, null=False, blank=False)
    description = models.CharField(max_length=255L, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)

    class Meta:
        db_table = 'fuel_types'
        managed = False
        verbose_name_plural = 'Заправки / Топливные компании'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class FuelCards(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    fuel_company = models.ForeignKey('FuelCompanies', null=False, blank=False)
    num = models.CharField(max_length=255L, null=False, blank=False)
    assigned_to_car = models.ForeignKey('car.Cars', null=True, blank=True)

    class Meta:
        db_table = 'fuel_cards'
        managed = False
        verbose_name_plural = 'Заправки / Топливные карты'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.num)


class RefuelsFlowManager(models.Manager):
    def get_queryset(self):
        return super(RefuelsFlowManager, self).get_queryset().select_related('driver', 'car', 'fuel_card')

    @staticmethod
    def list_with_run_checks(car_id, limit):
        query = """SELECT * FROM (
                      SELECT
                            R.date
                            ,R.km
                            ,R.type
                            ,R.amount
                            ,R.sum
                            ,R.comment
                            ,null as 'run_check'
                        FROM refuels_flow AS R
                        WHERE R.car_id = %s
                        UNION ALL
                        SELECT
                            C.date
                            ,C.km
                            ,""
                            ,""
                            ,""
                            ,C.comment
                            ,1
                        FROM run_checks_flow AS C
                        WHERE C.car_id = %s
                        ORDER BY date DESC LIMIT %s) AS reorder
                    ORDER BY date ASC
                    """
        limit = 10
        params = (car_id, car_id, limit)
        result = fetch_sql_allintuple(query, params=params)
        return result


class RefuelsFlow(models.Model):
    refuel_types = ([0, 'за наличные'], [1, 'покарте'])
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    fuel_type = models.ForeignKey('refuels.FuelTypes', null=False, blank=False, default=1)
    driver = models.ForeignKey('person.Employies', null=False, blank=False)
    car = models.ForeignKey('car.Cars', null=False, blank=False)
    fuel_card = models.ForeignKey('FuelCards', null=True, blank=True)
    type = models.IntegerField(null=False, blank=False, choices=refuel_types)
    amount = models.IntegerField(null=False, blank=False)
    sum = models.FloatField(null=False, blank=False)
    km = models.IntegerField(null=False, blank=False)
    comment = models.CharField(max_length=255L, null=True, blank=True)
    checked = models.IntegerField(blank=False, null=False, default=False)
    objects = RefuelsFlowManager()

    class Meta:
        db_table = 'refuels_flow'
        managed = False
        verbose_name_plural = 'Заправки / Все заправки'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.amount, self.sum)


class CarRunCheckFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey('person.Employies', null=False, blank=False)
    car = models.ForeignKey('car.Cars', null=False, blank=False)
    km = models.IntegerField(null=False, blank=False)
    comment = models.CharField(max_length=255L, null=True, blank=True)
    checked = models.IntegerField(blank=False, null=False, default=False)

    class Meta:
        db_table = 'run_checks_flow'
        managed = False
        verbose_name_plural = 'Заправки / Контроль пробега'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.date, self.km)