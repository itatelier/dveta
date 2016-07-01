# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents
from django.db import transaction
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


class FuelCards(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    fuel_company = models.ForeignKey('FuelCompanies', null=False, blank=False)
    num = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'fuel_cards'
        managed=False
        verbose_name_plural = 'Заправки / Топливные карты'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.num)


class RefuelsFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    driver = models.ForeignKey('person.Employies', null=False, blank=False)
    car = models.ForeignKey('car.Cars', null=False, blank=False)
    fuel_card = models.ForeignKey('FuelCards', null=True, blank=True)
    type = models.IntegerField(null=False, blank=False)
    amount = models.IntegerField(null=False, blank=False)
    summ = models.FloatField(null=False, blank=False)
    km = models.IntegerField(null=False, blank=False)
    comment = models.CharField(max_length=255L, null=True, blank=True)
    checked = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'refuels_flow'
        managed = False
        verbose_name_plural = 'Заправки / Все заправки'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.amount, self.summ)