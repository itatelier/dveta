# -*- coding: utf8 -*

from django.db import models


class RaceTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'race_types'
        verbose_name_plural = 'Рейсы / Типы рейсов'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class RaceCargoTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'race_cargo_types'
        verbose_name_plural = 'Рейсы / Типы груза'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class Races(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    car = models.ForeignKey('car.Cars', null=True, blank=True, editable=True, )
    driver = models.ForeignKey('person.Employies', null=True, blank=True, editable=True, )

    company = models.ForeignKey('company.Companies', null=False, blank=False, editable=True,)
    contragent = models.ForeignKey('contragent.Contragents', null=False, blank=False, editable=True,)

    race_type = models.ForeignKey('RaceTypes', null=True, blank=True, editable=True, )
    cargo_type = models.ForeignKey('RaceCargoTypes', null=True, blank=True, editable=True, )
    object = models.ForeignKey('object.Objects', null=True, blank=True, editable=True, )

    date_race = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    sum = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    pay_way = models.BooleanField()
    paid = models.BooleanField()

    hodkis = models.DecimalField(null=False, max_digits=2, decimal_places=0, blank=False, editable=True)

    bunker_type = models.ForeignKey('bunker.BunkerTypes', null=True, blank=True, editable=True, )
    bunker_qty = models.IntegerField(null=False, blank=False, editable=True)

    dump = models.ForeignKey('dump.Dumps', null=True, blank=True, editable=True, )
    dump_pay_type = models.BooleanField()
    dump_cash = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    dump_cash_extra = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    dump_cash_comment = models.CharField(max_length=200L, null=True, blank=True)
    dump_comment = models.CharField(max_length=200L, null=True, blank=True)
    recommendation = models.TextField(blank=True)

    date_add = models.DateTimeField(auto_now_add=True)

    mark_required = models.BooleanField()
    mark_done = models.BooleanField()
    mark_author = models.ForeignKey('person.Employies', null=True, blank=True, editable=True, related_name="race_marked")

    class Meta:
        db_table = 'races'
        verbose_name_plural = 'Рейсы'

    def __unicode__(self):
        return u'[%s]' % self.id
