# -*- coding: utf8 -*

from django.db import models


class CompanyAttractionSource(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'company_attraction_source'
        managed=False
        verbose_name_plural = 'Компании / Источник привлечения'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class CompanyRelTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'company_rel_types'
        managed=False
        verbose_name_plural = 'Компании / Типы отношений'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class CompanyOrgTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'company_org_types'
        managed=False
        verbose_name_plural = 'Компании / Типы организации'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class CompanyStatus(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255L, null=False, blank=False)
    css_class = models.CharField(max_length=255L, null=False, blank=False)

    class Meta:
        db_table = 'company_status'
        managed = False
        verbose_name_plural = 'Компании / Статусы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class ClientOptions(models.Model):
    request_tickets = models.BooleanField(blank=True, default=False)
    request_special_sign = models.BooleanField(blank=True, default=False)
    request_freq = models.IntegerField(blank=True, null=True, default=1)
    use_client_talons_only = models.BooleanField(blank=True, default=False)
    pay_condition = models.IntegerField(blank=True, null=True, default=1) # Условия оплаты 1=по постановке, 2=по вывозу
    pay_form = models.IntegerField(blank=True, null=True, default=1) # Форма оплаты 1=наличная, 2=безналичная
    pay_type = models.IntegerField(blank=True, null=True, default=1) # Тип оплаты 1=предоплата, 2=по факту
    credit_limit = models.IntegerField(blank=True, null=True, default=0)


    class Meta:
        managed = False
        db_table = 'client_options'
        verbose_name_plural = 'Опции клиента'


class Companies(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    www = models.CharField(max_length=255L, blank=True)
    org_type = models.ForeignKey('CompanyOrgTypes', null=False, blank=False)
    rel_type = models.ForeignKey('CompanyRelTypes', null=False, blank=False)
    attr_source = models.ForeignKey('CompanyAttractionSource', null=False, blank=False)
    status = models.ForeignKey('CompanyStatus', null=False, blank=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    client_options = models.OneToOneField('ClientOptions', null=True, blank=True, related_name='company')


    # objects = models.Manager()
    #main_branch = MainBranchManager()
    #is_active = models.CharField(max_length=255L, default=1, editable=False)

    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Компании'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)

'''
Branches
'''


class BranchTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=200L, null=False, blank=False)

    class Meta:
        db_table = 'branch_types'
        verbose_name_plural = 'Отделения / Типы'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)

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


class Branches(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255L)
    type = models.ForeignKey('BranchTypes', null=False, blank=True)
    company = models.ForeignKey('Companies', null=False, blank=True, editable=True, related_name='branches')
    address = models.OneToOneField('Addresses', null=False, blank=True, editable=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=1, editable=False)
    company_main = models.BooleanField(default=0, editable=False)

    class Meta:
        db_table = 'branches'
        verbose_name_plural = 'Отделения'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)

    # def main_phone(self):
    #     return self.branch_phone.filter(branch_main=1)

'''
Addresses
'''


class Addresses(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    # branch = models.ForeignKey('Branches', null=False, blank=True, related_name='address')
    postalcode = models.IntegerField(null=True, blank=True)
    city = models.CharField(max_length=255L, null=False, blank=False)
    street = models.CharField(max_length=255L, null=False, blank=False)
    app = models.CharField(max_length=255L, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    lat = models.FloatField(null=True, blank=True,)
    lng = models.FloatField(null=True, blank=True,)

    class Meta:
        db_table = 'addresses'
        verbose_name_plural = 'Адреса'

    def __unicode__(self):
        return u'%s, ул %s, %s' % (self.city, self.street, self.app)


class CompanyContacts(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    company = models.ForeignKey('company.Companies', null=False, blank=False, editable=True, related_name='contact')
    contact = models.ForeignKey('person.Contacts', null=False, blank=False, editable=True, related_name='contact')
    show_in_card = models.BooleanField(default=True, editable=True)
    company_main = models.BooleanField(default=0, editable=False)
    email = models.CharField(max_length=255L, blank=True, null=True)
    comment = models.CharField(max_length=255L, blank=True, null=True)
    role = models.CharField(max_length=255L, blank=True, null=True)

    class Meta:
        db_table = 'company_contacts'
        verbose_name_plural = 'Контакты компании'

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

