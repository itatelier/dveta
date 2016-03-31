# -*- coding: utf8 -*

from django.db import models


class DumpGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'dump_groups'
        verbose_name_plural = 'Полигоны / Группы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class Dumps(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    group = models.ForeignKey('DumpGroups', null=False, blank=False, editable=True, related_name='dumps')
    name = models.CharField(max_length=200L, null=False, blank=False)
    pay_type = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'dumps'
        verbose_name_plural = 'Полигоны'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DumpPrice(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    dump = models.ForeignKey('Dumps', null=False, blank=False, editable=True, related_name='price')
    price = models.DecimalField(decimal_places=0, max_digits=10, null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dump_price'
        verbose_name_plural = 'Полигоны / Цены'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.price, self.date_add)