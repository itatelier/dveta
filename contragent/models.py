# -*- coding: utf8 -*

from django.db import models


class ContragentGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = 'contragent_groups'
        verbose_name_plural = 'Контрагенты / Группы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class ContragentTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200, null=False, blank=False)

    class Meta:
        db_table = 'contragent_types'
        verbose_name_plural = 'Контрагенты / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class Contragents(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    company = models.ForeignKey('company.Companies', null=False, blank=True, editable=True, related_name='contragents')
    group = models.ForeignKey('ContragentGroups', null=False, blank=True)
    type = models.ForeignKey('ContragentTypes', null=False, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    inn = models.CharField(max_length=12, null=False, blank=True)
    kpp = models.CharField(max_length=9, null=False, blank=True)
    ogrn = models.CharField(max_length=13, null=False, blank=True)
    uraddress = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    company_default = models.BooleanField(null=False, blank=True, editable=True)

    class Meta:
        db_table = 'contragents'
        verbose_name_plural = 'Контрагенты'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)

# # class BankAccounts(models.Model):
# #     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
# #     bank_name = models.CharField(max_length=255, blank=True)
# #     bank_bik = models.CharField(max_length=9L, blank=True)
# #     bank_ks = models.CharField(max_length=20L, blank=True)
# #     bank_rs = models.CharField(max_length=20L, blank=True)
# #     date_add = models.DateTimeField(auto_now_add=True)
# #     date_update = models.DateTimeField(auto_now=True)
# #     contragent = models.ForeignKey('Contragents', null=False, blank=True, related_name='bank_accounts')
# #     comment = models.CharField(max_length=255, blank=True)
# #
# #     class Meta:
# #         db_table = 'bank_accounts'
# #         verbose_name_plural = 'Банковские счета'
# #
# #     def __unicode__(self):
# #         return u'[%s] %s %s' % (self.id, self.bank_name, self.bank_rs)
#

