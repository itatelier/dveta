# -*- coding: utf8 -*

from django.db import models
from django.contrib import admin


class CompanyTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'company_types'
        verbose_name_plural = 'Компании / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class MainBranchManager(models.Manager):
    def get_queryset(self):
        return super(MainBranchManager, self).get_queryset().branchmain.all()


class Companies(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255L)
    description = models.TextField(blank=True)
    www = models.CharField(max_length=255L, blank=True)
    type = models.ForeignKey('CompanyTypes', null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


    objects = models.Manager()
    #main_branch = MainBranchManager()
    #is_active = models.CharField(max_length=255L, default=1, editable=False)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Компании'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)

    #def json(self):
    #    return {
    #        'name': self.name,
    #        'date_add': self.date_add,
    #        'mainphone': [field.phone_number() for field in self.company_phone.all()]
    #    }

    #def mphone(self):
    #    return {
    #        'mainphone': [field.phone_number() for field in self.company_phone.all()]
    #    }

#
# class Addresses(models.Model):
#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     company = models.ForeignKey('Companies', null=False, blank=True, related_name='address')
#     # branch = models.ForeignKey('Branches', null=False, blank=True, related_name='address')
#     postalcode = models.IntegerField(max_length=255L, null=True, blank=True)
#     city = models.CharField(max_length=255L, null=False, blank=False)
#     street = models.CharField(max_length=255L, null=False, blank=False)
#     app = models.CharField(max_length=255L, null=True, blank=True)
#     app_extra = models.CharField(max_length=255L, blank=True, null=True)
#     comment = models.TextField(blank=True, null=True)
#     date_add = models.DateTimeField(auto_now_add=True)
#     date_update = models.DateTimeField(auto_now=True)
#     company_main = models.BooleanField(default=False, editable=False)
#
#     class Meta:
#         db_table = 'addresses'
#         verbose_name_plural = 'Адреса'
#
#     def __unicode__(self):
#         return u'[%s] %s, ул %s, дом %s %s' % (self.id, self.city, self.street, self.app, self.app_extra,)
#
#
# class BranchTypes(models.Model):
#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     name = models.CharField(max_length=200L, null=False, blank=False)
#
#     class Meta:
#         db_table = 'branch_types'
#         verbose_name_plural = 'Отделения / Типы'
#
#     def __unicode__(self):
#         return u'[%s] %s' % (self.id, self.name)
#
#
# class Branches(models.Model):
#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     name = models.CharField(max_length=255L)
#     type = models.ForeignKey('BranchTypes', null=False, blank=True)
#     company = models.ForeignKey('Companies', null=False, blank=True, editable=True, related_name='branches')
#     address = models.OneToOneField('Addresses', null=False, blank=True, editable=True)
#     date_add = models.DateTimeField(auto_now_add=True)
#     date_update = models.DateTimeField(auto_now=True)
#     description = models.TextField(blank=True, null=True)
#     is_active = models.BooleanField(default=1, editable=False)
#
#     class Meta:
#         db_table = 'branches'
#         verbose_name_plural = 'Отделения'
#
#     def __unicode__(self):
#         return u'[%s] %s' % (self.id, self.name)
#
#     def main_phone(self):
#         return self.branch_phone.filter(branch_main=1)
#
#
# class ContragentTypes(models.Model):
#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     name = models.CharField(max_length=200L, null=False, blank=False)
#
#     class Meta:
#         db_table = 'contragent_types'
#         verbose_name_plural = 'Контрагенты / Типы'
#
#     def __unicode__(self):
#         return u'[%s] %s' % (self.id, self.name)
#
#
# class Contragents(models.Model):
#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     company = models.ForeignKey('Companies', null=False, blank=True, editable=True, related_name='contragents')
#     type = models.ForeignKey('ContragentTypes', null=False, blank=True)
#     name = models.CharField(max_length=255L, null=False, blank=False)
#     inn = models.CharField(max_length=12L, null=False, blank=True)
#     kpp = models.CharField(max_length=9L, null=False, blank=True)
#     ogrn = models.CharField(max_length=13L, null=False, blank=True)
#     uraddress = models.CharField(max_length=255L, blank=True)
#     comment = models.CharField(max_length=255L, blank=True)
#     date_add = models.DateTimeField(auto_now_add=True)
#     date_update = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = 'contragents'
#         verbose_name_plural = 'Контрагенты'
#
#     def __unicode__(self):
#         return u'[%s] %s' % (self.id, self.name)
#
#
# class BankAccounts(models.Model):
#     id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
#     bank_name = models.CharField(max_length=255L, blank=True)
#     bank_bik = models.CharField(max_length=9L, blank=True)
#     bank_ks = models.CharField(max_length=20L, blank=True)
#     bank_rs = models.CharField(max_length=20L, blank=True)
#     date_add = models.DateTimeField(auto_now_add=True)
#     date_update = models.DateTimeField(auto_now=True)
#     contragent = models.ForeignKey('Contragents', null=False, blank=True, related_name='bank_accounts')
#     comment = models.CharField(max_length=255L, blank=True)
#
#     class Meta:
#         db_table = 'bank_accounts'
#         verbose_name_plural = 'Банковские счета'
#
#     def __unicode__(self):
#         return u'[%s] %s %s' % (self.id, self.bank_name, self.bank_rs)
#
#
# admin.site.register(Companies)
# admin.site.register(CompanyTypes)
# admin.site.register(Addresses)
# admin.site.register(Branches)
# admin.site.register(BranchTypes)
# admin.site.register(Contragents)
# admin.site.register(ContragentTypes)
# admin.site.register(BankAccounts)
#

