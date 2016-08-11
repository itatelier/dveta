# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *
from refuels.models import CarRunCheckFlow
from race.models import Races

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix, JsonUpdateObject
from django.http import HttpResponse


from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, Func, F
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import logging
log = logging.getLogger('django')


class SalaryMonthSummaryView(TemplateView):
    template_name = False
    report_month_dt = False
    report_prev_dt = False
    report_next_dt = False

    def dispatch(self, request, *args, **kwargs):
        # Месяц и год отчета будет предыдущий от даты "сегодня" или даты из запроса
        today = datetime.now()
        first_month_day = today.replace(day=1)  # прошлый месяц это 1е исло текщуго минус 1 день
        self.report_month_dt = first_month_day - timedelta(days=1)
        if request.GET.get('month') and request.GET.get('year'):
            try:
                self.report_month_dt = datetime.strptime("1/%s/%s" % (request.GET.get('month'), request.GET.get('year')), "%d/%m/%Y")
            except ValueError as err:
                log.info("- Month and Year params not good!")
        report_month_firstday = self.report_month_dt.replace(day=1)
        self.report_prev_dt = report_month_firstday - timedelta(days=1)
        self.report_next_dt = report_month_firstday + relativedelta(months=1)   # первое число следующего месяца
        return super(SalaryMonthSummaryView, self).dispatch(request, *args, **kwargs)


class SalaryMonthSummaryViewMech(SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_mech.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryView, self).get_context_data(*args, **kwargs)
        log.info("--- Month: %s   Year: %s" %(self.report_month_dt.month, self.report_month_dt.year))

        # Получаем список сформированных зарплатных листов за указанный месяц
        #  summary_list = SalaryMonthSummary.objects.filter(month__exact=self.report_month_dt.month, year__exact=self.report_month_dt.year).select_related('employee__person')
        context_data.update({
            'summary_list': SalaryMonthSummary.objects.drivers_list_races_and_summary(self.report_month_dt.date(), self.report_next_dt.date())
        })
        return context_data


class SalaryMonthSummaryPersonalView(SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_personal.html'
    employee_pk = False

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryPersonalView, self).get_context_data(*args, **kwargs)
        driver_pk = self.kwargs.get('driver_pk', None)
        context_data['driver'] = Employies.drivers.get(pk=driver_pk)
        context_data['stats_mech_checkups'] = CarRunCheckFlow.objects.filter(date__month=self.report_month_dt.month, date__year=self.report_month_dt.year, driver_id=driver_pk).count()
        context_data['stats_races'] = Races.objects.filter(date_race__month=self.report_month_dt.month, date_race__year=self.report_month_dt.year, driver_id=driver_pk).count()
        context_data['stats_hodkis'] = Races.objects.filter(date_race__month=self.report_month_dt.month, date_race__year=self.report_month_dt.year, driver_id=driver_pk).aggregate(Sum('hodkis'))['hodkis__sum']

        # Список месячных показателей по каждой машине
        log.info("--- Report date_start: %s  date_end: %s" % (self.report_month_dt.date(), self.report_next_dt.date()))
        driver_month_stats = SalaryMonthSummary.objects.driver_month_stats(date_start=self.report_month_dt.date(), date_end=self.report_next_dt.date(), driver_pk=driver_pk)
        context_data['driver_month_stats'] = driver_month_stats

        # Перечень всех сверок за месяц (список водителей слева)

        summary_list = SalaryMonthSummary.objects.drivers_list_races_and_summary(self.report_month_dt.date(), self.report_next_dt.date())
        context_data['summary_list'] = summary_list
        log.info("== data: %s" % summary_list)
        average_stats = {}
        for k in driver_month_stats:
            average_stats['total_races'] = k.total_races

        log.info("= %s" % average_stats['total_races'])
        # if len(summary_list.data.keys()) > 1:
        #     average_stats['a_km_on_100'] = 1
        #
        # context_data['average_stats'] = average_stats
        return context_data
