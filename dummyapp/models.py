# -*- coding: utf8 -*

from django.db import models


class DummyCompanies(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    www = models.CharField(max_length=255L, blank=True)
    org_type = models.ForeignKey('CompanyOrgTypes', null=False, blank=False)
    rel_type = models.ForeignKey('CompanyRelTypes', null=False, blank=False)
    status = models.ForeignKey('CompanyStatus', null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Тестирование / Компании'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)