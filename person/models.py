# -*- coding: utf8 -*

from django.db import models
from django.core.urlresolvers import reverse


class Persons(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    family_name = models.CharField(max_length=255L, null=False, blank=False)
    given_name = models.CharField(max_length=255L, null=False, blank=False)
    middle_name = models.CharField(max_length=255L, blank=True, null=True)
    nick_name = models.CharField(max_length=255L, blank=True, null=True)
    date_ofbirth = models.DateTimeField(null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'persons'
        verbose_name_plural = 'Персоны'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.nick_name)

    def get_absolute_url(self):
        return reverse('person_card', kwargs={'pk': self.pk})


class Contacts(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    role = models.CharField(max_length=255L, blank=True, null=True)
    email = models.CharField(max_length=255L, blank=True, null=True)
    comment = models.CharField(max_length=255L, blank=True, null=True)
    phonenumber = models.CharField(max_length=255L, blank=True, null=True)
    is_work = models.BooleanField(default=0, editable=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('company.Companies', null=True, blank=True, editable=True, related_name='contacts')
    person = models.ForeignKey('Persons', null=True, blank=True, editable=True, related_name='contacts')
    company_main = models.BooleanField(default=0, editable=False)

    class Meta:
        db_table = 'contacts'
        verbose_name_plural = 'Контакты'

    def __unicode__(self):
        return u'[%s] %s %s' % (self.id, self.person.nick_name, self.company.name)
