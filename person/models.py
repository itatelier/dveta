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
        return u'%s %s (%s)' % (self.family_name, self.given_name, self.nick_name)

    def fio_and_nick(self):
        return u'%s %s (%s)' % (self.family_name, self.given_name, self.nick_name)

    def get_absolute_url(self):
        return reverse('person_card', kwargs={'pk': self.pk})


class Contacts(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    phonenumber = models.CharField(max_length=255L, blank=True, null=True)
    is_work = models.BooleanField(default=0, editable=False)
    is_main = models.BooleanField(default=0, editable=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    # company = models.ForeignKey('company.Companies', null=True, blank=True, editable=True, related_name='contacts')
    person = models.ForeignKey('Persons', null=True, blank=True, editable=True, related_name='contacts')

    class Meta:
        db_table = 'contacts'
        verbose_name_plural = 'Контакты'




class EmployeeTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'employee_types'
        verbose_name_plural = 'Сотрудники / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class EmployeeRoles(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'employee_roles'
        verbose_name_plural = 'Сотрудники / Роли'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class EmployeeStatuses(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'employee_statuses'
        verbose_name_plural = 'Сотрудники / Статусы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class EmployeeDriversManager(models.Manager):
    def get_queryset(self):
        return super(EmployeeDriversManager, self).get_queryset().select_related('person').filter(role__pk=2)


class EmployeeMechanicsManager(models.Manager):
    def get_queryset(self):
        return super(EmployeeMechanicsManager, self).get_queryset().select_related('person').filter(role__pk=3)


class EmployeeManagerManager(models.Manager):
    def get_queryset(self):
        return super(EmployeeManagerManager, self).get_queryset().select_related('person').filter(role__pk=4)


class EmployeeAllDefaultManager(models.Manager):
    def get_queryset(self):
        return super(EmployeeAllDefaultManager, self).get_queryset().select_related('person', 'role', 'type', 'status')


class Employies(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    person = models.ForeignKey('Persons', null=False, blank=False)
    type = models.ForeignKey('EmployeeTypes', null=False, blank=False)
    role = models.ForeignKey('EmployeeRoles', null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=250L, null=True, blank=True)
    status = models.ForeignKey('EmployeeStatuses', null=True, blank=True)
    objects = EmployeeAllDefaultManager()
    drivers = EmployeeDriversManager()
    mechanics = EmployeeMechanicsManager()
    managers = EmployeeManagerManager()

    class Meta:
        db_table = 'employies'
        verbose_name_plural = 'Сотрудники'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.role)

    def fullname(self):
        return u'%s %s' % (self.person.family_name, self.person.given_name)

class Driverss(Employies):
    objects = EmployeeAllDefaultManager()

    class Meta:
        verbose_name_plural = 'Водители'
        db_table = 'employies'


class UnitGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)
    description = models.CharField(max_length=250L, null=True, blank=True)

    class Meta:
        db_table = 'unit_groups'
        verbose_name_plural = 'Сотрудники / Группы'

    def __unicode__(self):
        return u'%s' % self.description
