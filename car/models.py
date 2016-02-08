# -*- coding: utf8 -*

from django.db import models
from django.core.urlresolvers import reverse


class CarBrands(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'car_brands'
        verbose_name_plural = 'Машины / Марки'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class CarModels(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)
    brand = models.ForeignKey('CarBrands', null=True, blank=True, editable=True, related_name='brand')
    description = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'car_models'
        verbose_name_plural = 'Машины / Модели'

    def __unicode__(self):
        return u'[%s] %s' % (self.val, self.description)


class CarFuelTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'car_fuel_types'
        verbose_name_plural = 'Машины / Типы топлива'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class Cars(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    reg_num = models.CharField(max_length=200L, null=False, blank=False)
    nick_name = models.CharField(max_length=200L, null=False, blank=False)
    model = models.ForeignKey('CarModels', null=False, blank=False, editable=True)
    fuel_type = models.ForeignKey('CarFuelTypes', null=False, blank=False, editable=True)
    mechanic = models.ForeignKey('person.Employies', null=False, blank=False, editable=True)
    unit_group = models.ForeignKey('person.UnitGroups', null=False, blank=False, editable=True)
    fuel_norm = models.IntegerField(blank=True, null=True, default=0)
    trailer_attached = models.IntegerField(blank=True, null=True, default=0)

    class Meta:
        db_table = 'cars'
        verbose_name_plural = 'Машины'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.reg_num, self.nick_name)
