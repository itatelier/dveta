# -*- coding: utf8 -*

from person.forms import *
from forms import *
# App spcific
from models import *
from company.models import *
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
        #  summary_list = Sal
        # aryMonthSummary.objects.filter(month__exact=self.report_month_dt.month, year__exact=self.report_month_dt.year).select_related('employee__person')
        context_data['summary_list'] = SalaryMonthSummary.objects.drivers_list_races_and_summary(self.report_month_dt.date(), self.report_next_dt.date())
        return context_data


class SalaryMonthSummaryPersonalView(UpdateView, SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_personal.html'
    driver_pk = False
    form_class = SalaryMechCheckForm
    model = SalaryMonthSummary
    object = None
    prepared_data = None

    def prepare_data(self):
        prepared_data = {}
        prepared_data['driver'] = Employies.drivers.get(pk=self.driver_pk)
        prepared_data['stats_mech_checkups'] = CarRunCheckFlow.objects.filter(date__month=self.report_month_dt.month, date__year=self.report_month_dt.year, driver_id=self.driver_pk).count()
        prepared_data['stats_races'] = Races.objects.filter(date_race__month=self.report_month_dt.month, date_race__year=self.report_month_dt.year, driver_id=self.driver_pk).count()
        prepared_data['stats_hodkis'] = Races.objects.filter(date_race__month=self.report_month_dt.month, date_race__year=self.report_month_dt.year, driver_id=self.driver_pk).aggregate(Sum('hodkis'))['hodkis__sum']

        # Список месячных показателей по каждой машине
        driver_month_stats = SalaryMonthSummary.objects.driver_month_stats(date_start=self.report_month_dt.date(), date_end=self.report_next_dt.date(), driver_pk=self.driver_pk)
        prepared_data['driver_month_stats'] = driver_month_stats
        report_stats = {}
        average_and_sum_stats = {'fuel_overuse': 0}
        report_stats_keys = ['races_done', 'total_hodkis', 'total_refuels', 'total_amount', 'total_run', 'lit_on_100', 'km_on_hodkis']
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
                average_and_sum_stats['km_on_hodkis'] = report_stats['km_on_hodkis']['value'] / report_stats['km_on_hodkis']['count']
            if report_stats['lit_on_100']['count'] > 0:
                average_and_sum_stats['average_consumption'] = "%.1f" % (report_stats['lit_on_100']['value'] / report_stats['lit_on_100']['count'])
            prepared_data['average_and_sum_stats'] = average_and_sum_stats
        return prepared_data

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryPersonalView, self).get_context_data(*args, **kwargs)
        context_data.update(self.prepared_data)
        return context_data

    def get_object(self, *args, **kwargs):
        try:
            exist_object = SalaryMonthSummary.objects.get(
                employee_id=self.driver_pk,
                year=self.report_month_dt.year,
                month=self.report_month_dt.month
            )
            return exist_object
        except SalaryMonthSummary.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        # получаем объект формы
        self.driver_pk = self.kwargs.get('driver_pk', None)
        self.object = self.get_object(self, *args, **kwargs)
        self.prepared_data = self.prepare_data()
        if not self.object:
            form_initial = {}
            if 'average_and_sum_stats' in self.prepared_data:
                for key, val in self.prepared_data['average_and_sum_stats'].items():
                    form_initial[key] = val
                    log.info("=== Initial %s : %s" % (key, val))
            self.initial = form_initial
        #return super(SalaryMonthSummaryPersonalView, self).get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.driver_pk = self.kwargs.get('driver_pk', None)
        self.object = self.get_object(self, *args, **kwargs)
        form = self.get_form()
        if form.is_valid():
            if not self.object:
                create_object = form.save(commit=False)
                create_object.year = self.report_month_dt.year
                create_object.month = self.report_month_dt.month
                create_object.employee = Employies(pk=self.driver_pk)
                create_object.check_status = 1
                # create_object.s
                create_object.save()
            else:
                self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = form.instance
            self.prepared_data = self.prepare_data()
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return "%s?year=%s&month=%s" % (reverse('salary_month_summary_mech'), self.report_month_dt.year, self.report_month_dt.month)


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


class SalaryOperationCreateView(LoginRequiredMixin, CreateView):
    template_name = 'salary/salary_operation_create.html'
    form_class = SalaryOperationCreateForm
    model = SalaryFlow
    object = None

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return '/'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryOperationCreateView, self).get_context_data(*args, **kwargs)
        context_data['employee'] = Employies.objects.get(pk=self.kwargs.get('employee_pk'))
        return context_data

    def get_form_kwargs(self):
        kwargs = super(SalaryOperationCreateView, self).get_form_kwargs()
        kwargs.update({
            'year': self.kwargs.get('year', None),
            'month': self.kwargs.get('month', None),
            'operation_type': self.kwargs.get('type_pk', None),
            'employee': self.kwargs.get('employee_pk', None),
        })
        return kwargs
