# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from common.forms import *
from datetime import datetime, timedelta
from race.models import *
from dds.models import *
from person.models import Employies


class WorkdayBaseView(LoginRequiredMixin, TemplateView):
    driver_pk = False
    date = False

    def dispatch(self, request, *args, **kwargs):
        self.driver_pk = self.kwargs.get('driver_pk', False)
        self.date = datetime.strptime(self.kwargs.get('date', False), '%d-%m-%y')
        return super(WorkdayBaseView, self).dispatch(request, *args, **kwargs)

    def driver(self):
        return Employies.objects.get(pk=self.driver_pk)

    # def stats(self):
    #     stats = {
    #         'balance': DdsAccounts.objects.get(employee=self.driver_pk).balance,
    #         'summ_income': DdsFlow.objects.filter(
    #             account__employee=self.driver_pk,
    #             date__lte=self.date.date()
    #         ).aggregate(Sum('summ')),
    #         'summ_end_of_day': DdsFlow.objects.filter(
    #             date__range=(self.date.date(), self.date.date() + timedelta(days=1)),
    #             account__employee=self.driver_pk
    #         ).aggregate(Sum('summ'))
    #     }
    #     return stats


class WorkdayRacesView(WorkdayBaseView):
    template_name = 'workday/workday_races.html'

    def races(self):
        return Races.objects.filter(
            driver=self.driver_pk,
            date_race__day=self.date.day,
            date_race__month=self.date.month,
            date_race__year=self.date.year,
        ).select_related('object', 'dump', 'company', 'race_type', 'cargo_type', 'bunker_type')


class WorkdayDdsView(WorkdayBaseView):
    template_name = 'workday/workday_dds.html'

    # def dds_flow(self):
    #     return DdsFlow.objects.filter(account__employee__pk=self.driver_pk).select_related('account', 'item')

    def get_context_data(self, *args, **kwargs):
        context_data = super(WorkdayDdsView, self).get_context_data(*args, **kwargs)
        context_data.update({
            'dds_flow':     DdsFlow.objects.filter(account__employee__pk=self.driver_pk).select_related('account', 'item'),
            'balance':      DdsAccounts.objects.get(employee=self.driver_pk).balance,
            'summ_income':  DdsFlow.objects.filter(
                                account__employee=self.driver_pk,
                                date__lte=self.date.date()
                            ).aggregate(Sum('summ'))['summ__sum'],
            'summ_end_of_day': DdsFlow.objects.filter(
                                date__range=(self.date.date(), self.date.date() + timedelta(days=1)),
                                account__employee=self.driver_pk
                            ).aggregate(Sum('summ'))['summ__sum']
        })
        context_data['balance'] = context_data['summ_income'] + context_data['summ_end_of_day']
        context_data['templates'] = DdsTemplates.objects.filter(group=2).values_list('pk', 'name', 'comment')
        return context_data


