# -*- coding: utf8 -*

from django.db import models


class ObjectTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'object_types'
        verbose_name_plural = 'Объекты / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class Objects(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=200L, null=False, blank=False)
    type = models.ForeignKey('ObjectTypes', null=False, blank=False, editable=True)
    company = models.ForeignKey('company.Companies', null=False, blank=False, editable=True)
    address = models.ForeignKey('company.Addresses', null=False, blank=False, editable=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'objects'
        verbose_name_plural = 'Объекты'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)
