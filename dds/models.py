# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents

class DdsItemGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'dds_item_groups'
        managed=False
        verbose_name_plural = 'Деньги / Группы статей'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DdsItems(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    item_group = models.ForeignKey('DdsItemGroups', null=False, blank=False)
    name = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'dds_items'
        managed=False
        verbose_name_plural = 'Деньги / Статьи учета'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DdsAccountTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'dds_item_groups'
        managed=False
        verbose_name_plural = 'Деньги / Типы счетов'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class DdsAccounts(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    type = models.ForeignKey('DdsAccountTypes', null=False, blank=False)
    employee = models.ForeignKey('person.Employies', null=True, blank=True)
    contragent = models.ForeignKey('contragent.Contragents', null=True, blank=True)
    balance = models.FloatField(default=0, null=True, blank=True, )

    class Meta:
        db_table = 'dds_accounts'
        managed=False
        verbose_name_plural = 'Деньги / Счета'

    def __unicode__(self):
        return u'[%s] %s %s %s %s ' % (self.id, self.type, self.employee, self.contragent, self.balance)


class DdsFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    parent_op = models.ForeignKey('self', null=True, blank=True)
    item = models.ForeignKey('DdsItems', null=False, blank=False)
    account = models.ForeignKey('DdsAccounts', null=False, blank=False)
    summ = models.FloatField(default=0, null=True, blank=True, )

    class Meta:
        db_table = 'dds_flow'
        managed=False
        verbose_name_plural = 'Деньги / Движение'

    def __unicode__(self):
        return u'[%s] %s %s %s %s' % (self.id, self.date_add, self.item, self.account, self.summ)
