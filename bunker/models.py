# -*- coding: utf8 -*

from django.db import models


class BunkerTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'bunker_types'
        verbose_name_plural = 'Бункеры / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class BunkerOperationTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'bunker_operation_types'
        verbose_name_plural = 'Бункеры / Типы операций'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class BunkerFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    object = models.ForeignKey('object.Objects', null=False, blank=False, editable=True)
    operation_type = models.ForeignKey('bunker.BunkerOperationTypes', null=False, blank=False, editable=True)
    bunker_type = models.ForeignKey('bunker.BunkerTypes', null=False, blank=False, editable=True)
    qty = models.IntegerField(null=False, blank=False, editable=True)

    class Meta:
        db_table = 'bunker_flow'
        verbose_name_plural = 'Бункеры / Движение'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.date, self.qty)
