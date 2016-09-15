# -*- coding: utf8 -*

from django.db import models
from django.core.urlresolvers import reverse
from object.models import Objects


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


class CarLoadTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'car_load_types'
        verbose_name_plural = 'Машины / Типы по загрузке'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class CarStatuses(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'car_status'
        verbose_name_plural = 'Машины / Статусы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class Cars(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    reg_num = models.CharField(max_length=200L, null=False, blank=False)
    nick_name = models.CharField(max_length=200L, null=False, blank=False)
    comment = models.CharField(max_length=200L, null=False, blank=False)
    model = models.ForeignKey('CarModels', null=False, blank=False, editable=True)
    fuel_type = models.ForeignKey('CarFuelTypes', null=False, blank=False, editable=True)
    load_type = models.ForeignKey('CarLoadTypes', null=False, blank=False, editable=True)
    mechanic = models.ForeignKey('person.Employies', null=False, blank=False, editable=True, related_name="carmechanic")
    unit_group = models.ForeignKey('person.UnitGroups', null=False, blank=False, editable=True)
    fuel_norm = models.IntegerField(blank=True, null=True, default=0)
    trailer_attached = models.IntegerField(blank=True, null=True, default=0)
    car_object = models.ForeignKey('object.Objects', null=False, blank=False, editable=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('CarStatuses', null=False, blank=False, editable=True)
    driver = models.ForeignKey('person.Employies', null=True, blank=True, editable=True, related_name="cardriver")
    docs = models.ForeignKey('CarDocs', null=True, blank=False, editable=True, related_name="car")
    fuel_card = models.ForeignKey('refuels.FuelCards', null=True, blank=True, editable=True, related_name="driver")

    class Meta:
        db_table = 'cars'
        verbose_name_plural = 'Машины'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.reg_num, self.nick_name)


class CarOwners(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'car_owners'
        verbose_name_plural = 'Машины / Владельцы'

    def __unicode__(self):
        return self.val


class CarDocs(models.Model):
    owner = models.ForeignKey('CarOwners', null=True, blank=False)
    ins_date_register = models.DateTimeField(blank=True, null=True)
    ins_number = models.CharField(max_length=255, blank=True, null=True)
    ins_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    ins_date_end = models.DateTimeField(blank=True, null=True)
    ins_comment = models.CharField(max_length=255, blank=True, null=True)
    to_number = models.CharField(max_length=255, blank=True, null=True)
    to_date_end = models.DateTimeField(blank=True, null=True)
    rent_date_end = models.DateTimeField(blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'car_docs'
        verbose_name_plural = 'Машины / Документы'
