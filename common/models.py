# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents
from django.db import transaction
from django.db.models import F


class Variables(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    var = models.CharField(max_length=255, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    val = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = 'variables'
        managed=False
        verbose_name_plural = 'Система / Переменные'

    def __unicode__(self):
        return u'[%s] %s %s %s' % (self.id, self.var, self.name, self.val)

