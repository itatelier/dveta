# -*- coding: utf8 -*

from django.db import models
from person.models import Employies
from contragent.models import Contragents
from django.db import transaction
from django.db.models import F


class DdsItemGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'dds_item_groups'
        managed=False
        verbose_name_plural = 'Деньги / Группы статей'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DdsItems(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    item_group = models.ForeignKey('DdsItemGroups', null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    direction_type = models.BooleanField(default=False,  editable=True, blank=True)

    class Meta:
        db_table = 'dds_items'
        managed=False
        verbose_name_plural = 'Деньги / Статьи учета'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DdsAccountTypes(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    val = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'dds_account_types'
        managed=False
        verbose_name_plural = 'Деньги / Типы счетов'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.val)


class AccountManager(models.Manager):

    def update_balance(self, pk, summ):
        with transaction.atomic():
            self.select_for_update().filter(pk=pk).update(balance=F('balance')+summ)
        return self


class DdsAccounts(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey('dds.DdsAccountTypes', null=False, blank=False)
    employee = models.ForeignKey('person.Employies', null=True, blank=True, related_name='money_account')
    contragent = models.ForeignKey('contragent.Contragents', null=True, blank=True, related_name='money_account')
    balance = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, default=0)
    status = models.BooleanField()
    objects = AccountManager()

    class Meta:
        db_table = 'dds_accounts'
        managed=False
        verbose_name_plural = 'Деньги / Счета'

    def __unicode__(self):
        return u'[%s] %s %s %s %s' % (self.id, self.employee, self.contragent, self.balance, self.type)


class FlowManager(models.Manager):
    def flow_op(self, item_id, account_id, pay_way, summ, op_type):
        with transaction.atomic():
            DdsAccounts.objects.select_for_update().filter(pk=account_id).update(balance=F('balance')+summ)
            flowop = self.create(
                item=DdsItems(pk=item_id),
                account=DdsAccounts(pk=account_id),
                pay_way=True,
                summ=summ,
                op_type=op_type
            )
        return flowop

    def flow_move(self, item_out_id, account_out_id, pay_way_out, item_in_id, account_in_id, pay_way_in,  summ):
        with transaction.atomic():
            # Обновляем баланс исходящего счета
            DdsAccounts.objects.select_for_update().filter(pk=account_out_id).update(balance=F('balance')+summ*(-1))
            # Обновляем баланс входящего счета
            DdsAccounts.objects.select_for_update().filter(pk=account_in_id).update(balance=F('balance')+summ)
            # Запись в потоке для исходящей операции
            flow_object_out = DdsFlow(
                item=DdsItems(pk=item_out_id),
                account=DdsAccounts(pk=account_out_id),
                pay_way=pay_way_out,
                summ=summ,
                op_type=False
            )
            flow_object_out.save()
            # Запись в потоке для входящей операции
            flow_object_in = DdsFlow(
                item=DdsItems(pk=item_in_id),
                account=DdsAccounts(pk=account_in_id),
                pay_way=pay_way_out,
                parent_op=flow_object_out,
                summ=summ,
                op_type=True
            )
            flow_object_in.save()
        return True


class DdsFlow(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    parent_op = models.ForeignKey('self', null=True, blank=True)
    item = models.ForeignKey('DdsItems', null=False, blank=False)
    account = models.ForeignKey('DdsAccounts', null=False, blank=False)
    summ = models.DecimalField(default=0, null=True, decimal_places=0, max_digits=10, blank=True)
    op_type = models.BooleanField(default=False)  # тип операции над счетом (1 приход, 0 расход)
    pay_way = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    objects = FlowManager()

    class Meta:
        db_table = 'dds_flow'
        managed = False
        verbose_name_plural = 'Деньги / Движение'

    def __unicode__(self):
        return u'[%s] %s %s %s %s' % (self.id, self.date, self.item.pk, self.account.pk, self.summ)


class DdsTemplateGroups(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'dds_template_groups'
        managed=False
        verbose_name_plural = 'Деньги / Группы шаблонов операций'

    def __unicode__(self):
        return u'[%s] %s' % (self.id, self.name)


class DdsTemplates(models.Model):
    id = models.AutoField(unique=True, primary_key=True, null=False, blank=False)
    group = models.ForeignKey('dds.DdsTemplateGroups', null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    item_out = models.ForeignKey('DdsItems', null=True, blank=True, related_name='template_item_out')
    account_out = models.ForeignKey('DdsAccounts', null=True, blank=True, related_name='template_account_out')
    account_out_required = models.BooleanField(default=False)
    account_out_visible = models.BooleanField(default=True)
    item_in = models.ForeignKey('DdsItems', null=True, blank=True, related_name='template_item_in')
    account_in = models.ForeignKey('DdsAccounts', null=True, blank=True, related_name='template_account_in')
    account_in_required = models.BooleanField(default=False)
    account_in_visible = models.BooleanField(default=True)
    summ = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True, default=0)
    pay_way = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'dds_templates'
        managed = False
        verbose_name_plural = 'Деньги / Шаблоны'
