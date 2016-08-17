# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *
from refuels.models import CarRunCheckFlow
from race.models import Races
from car.models import Cars

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
        self.report_month_dt = (first_month_day - timedelta(days=1)).replace(day=1)  # первый день прошлого месяца
        if request.GET.get('month') and request.GET.get('year'):
            try:
                self.report_month_dt = datetime.strptime("1/%s/%s" % (request.GET.get('month'), request.GET.get('year')), "%d/%m/%Y")
            except ValueError as err:
                log.info("- Month and Year params not good!")
        report_month_firstday = self.report_month_dt.replace(day=1)
        self.report_prev_dt = report_month_firstday - timedelta(days=1)
        self.report_next_dt = report_month_firstday + relativedelta(months=1)   # первое число следующего месяца
        log.info("--- Report period starts at: %s till end date:  %s" %(self.report_month_dt.date(), self.report_next_dt.date()))
        return super(SalaryMonthSummaryView, self).dispatch(request, *args, **kwargs)


class SalaryMonthSummaryViewMech(SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_mech.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryView, self).get_context_data(*args, **kwargs)
        # Получаем список сформированных зарплатных листов за указанный месяц
        #  summary_list = SalaryMonthSummary.objects.filter(month__exact=self.report_month_dt.month, year__exact=self.report_month_dt.year).select_related('employee__person')
        context_data['summary_list'] = SalaryMonthSummary.objects.drivers_list_races_and_summary(self.report_month_dt.date(), self.report_next_dt.date())
        return context_data


class SalaryMonthSummaryPersonalView(CreateView, SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_personal.html'
    employee_pk = False
    form_class = SalaryMechCheckForm
    model = SalaryMonthSummary
    object = None

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryPersonalView, self).get_context_data(*args, **kwargs)
        driver_pk = self.kwargs.get('driver_pk', None)
        context_data['driver'] = Employies.drivers.get(pk=driver_pk)
        context_data['stats_mech_checkups'] = CarRunCheckFlow.objects.filter(date__month=self.report_month_dt.month, date__year=self.report_month_dt.year, driver_id=driver_pk).count()
        context_data['stats_races'] = Races.objects.filter(date_race__month=self.report_month_dt.month, date_race__year=self.report_month_dt.year, driver_id=driver_pk).count()
        context_data['stats_hodkis'] = Races.objects.filter(date_race__month=self.report_month_dt.month, date_race__year=self.report_month_dt.year, driver_id=driver_pk).aggregate(Sum('hodkis'))['hodkis__sum']

        # Список месячных показателей по каждой машине
        driver_month_stats = SalaryMonthSummary.objects.driver_month_stats(date_start=self.report_month_dt.date(), date_end=self.report_next_dt.date(), driver_pk=driver_pk)
        context_data['driver_month_stats'] = driver_month_stats
        report_stats = {}
        average_and_sum_stats = {'fuel_overuse': 0}
        report_stats_keys = ['total_races', 'total_hodkis', 'total_refuels', 'total_amount', 'total_run', 'lit_on_100', 'km_on_hodkis']
        report_len = len(driver_month_stats)
        if report_len > 0:
            for key in report_stats_keys:
                report_stats[key] = {'value': 0, 'count': 0}
                for row in driver_month_stats:
                    if row._asdict()[key] is not None:
                        report_stats[key]['value'] += row._asdict()[key]
                        report_stats[key]['count'] += 1
                average_and_sum_stats[key] = report_stats[key]['value']
            for row in driver_month_stats:
                if row._asdict()['fuel_overuse'] > 0:
                    average_and_sum_stats['fuel_overuse'] += row._asdict()['fuel_overuse']
            if report_stats['km_on_hodkis']['count'] > 0:
                average_and_sum_stats['average_km_on_hodka'] = report_stats['km_on_hodkis']['value'] / report_stats['km_on_hodkis']['count']
            if report_stats['lit_on_100']['count'] > 0:
                average_and_sum_stats['average_lit_on_100'] = report_stats['lit_on_100']['value'] / report_stats['lit_on_100']['count']
                log.info("=!= %s / %s = %s " % (
                    report_stats['lit_on_100']['value'],
                    report_stats['lit_on_100']['count'],
                    average_and_sum_stats['average_lit_on_100']
                ))

            for k in report_stats_keys:
                log.info("= %s: value: %s  count: %s" % (k, report_stats[k]['value'], report_stats[k]['count']))
            for k, v in average_and_sum_stats.items():
                log.info("=== Averaga %s: %s" % (k, v))
            context_data['average_and_sum_stats'] = average_and_sum_stats
        return context_data


class SalaryMonthSummaryCarRefuelsView(SalaryMonthSummaryView):
    template_name = 'salary/salary_month_refuels_bycar.html'
    employee_pk = False

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryCarRefuelsView, self).get_context_data(*args, **kwargs)
        car_pk = self.kwargs.get('car_pk', None)
        context_data['car'] = Cars.objects.get(pk=car_pk)
        refuels_on_period_for_car =  SalaryMonthSummary.objects.refuels_on_period_for_car(date_start=self.report_month_dt.date(), date_end=self.report_next_dt.date(), car_pk=car_pk)
        context_data['refuels_on_period_for_car'] = refuels_on_period_for_car
        return context_data
