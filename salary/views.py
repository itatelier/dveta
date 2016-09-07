# -*- coding: utf8 -*

from person.forms import *
from forms import *
# App spcific
from models import *
from company.models import *
from refuels.models import CarRunCheckFlow
from race.models import Races
from car.models import Cars
from common.models import Variables

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix, JsonUpdateObject
from django.http import HttpResponse


from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Count, Func, F
import calendar


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
    template_name = 'salary/salary_month_summary_mechanic.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryView, self).get_context_data(*args, **kwargs)
        # Получаем список сформированных зарплатных листов за указанный месяц
        #  summary_list = Sal
        # aryMonthSummary.objects.filter(month__exact=self.report_month_dt.month, year__exact=self.report_month_dt.year).select_related('employee__person')
        context_data['summary_list'] = SalaryMonthSummary.objects.drivers_list_races_and_summary(self.report_month_dt.date(), self.report_next_dt.date())
        return context_data


class SalaryMonthAnalyzeMechanicView(UpdateView, SalaryMonthSummaryView):
    template_name = 'salary/salary_month_analyze_mechanic.html'
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
            # Начисления бонусов и штрафов
            prepared_data['accruals_list'] = SalaryFlow.objects.filter(employee=self.driver_pk, year=self.report_month_dt.year, month=self.report_month_dt.month).select_related('operation_name')
        return prepared_data

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthAnalyzeMechanicView, self).get_context_data(*args, **kwargs)
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
            self.initial = form_initial
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
                # if create_object.operation_type in ()
                # create_object.check_status = 1
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
    operation_type = False
    operation_type_object = False
    operation_direction = False

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return '/'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryOperationCreateView, self).get_context_data(*args, **kwargs)
        context_data['employee'] = Employies.objects.get(pk=self.kwargs.get('employee_pk'))
        context_data['operation_type_object'] = self.operation_type_object
        return context_data

    def get_form_kwargs(self):
        kwargs = super(SalaryOperationCreateView, self).get_form_kwargs()
        self.operation_type = self.kwargs.get('type_pk', None)
        kwargs.update({
            'year': self.kwargs.get('year', None),
            'month': self.kwargs.get('month', None),
            'operation_type': self.operation_type,
            'employee': self.kwargs.get('employee_pk', None),
        })
        # Направление начисление - плюс или минус
        if self.operation_type:
            self.operation_type_object = SalaryOperationTypes.objects.get(pk=self.operation_type)
            self.operation_direction = self.operation_type_object.direction
            kwargs.update({'operation_direction': self.operation_direction})
        return kwargs


class SalaryMonthSummaryViewOffice(SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_office.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryView, self).get_context_data(*args, **kwargs)
        log.info("--- QS Y: %s M:%s" % (
            self.report_month_dt.year,
            self.report_month_dt.month
        ))
        context_data['summary_list'] = SalaryMonthSummary.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, check_status__in=(2, 3))
        return context_data


class SalaryMonthAnalyzeOfficeView(UpdateView, SalaryMonthSummaryView):
    template_name = 'salary/salary_month_analyze_office.html'
    driver_pk = False
    form_class = SalaryMechCheckForm
    model = SalaryMonthSummary
    object = None
    prepared_data = None

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

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthAnalyzeOfficeView, self).get_context_data(*args, **kwargs)
        context_data['driver'] = Employies.drivers.get(pk=self.driver_pk)
        # список всех начислений
        context_data['accruals_list'] = SalaryFlow.objects.filter(
            employee=self.driver_pk,
            year=self.report_month_dt.year,
            month=self.report_month_dt.month).select_related('operation_name')
        # Суммарные показатели начислений (group_by type)
        context_data['accruals_summary'] = SalaryFlow.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type__in=(2, 3, 4, 5)).values_list('operation_type__type').annotate(total=Sum('sum'))
        accruals_sum = 0
        for el in context_data['accruals_summary']:
            accruals_sum += el[1]
        context_data['accruals_sum'] = accruals_sum
        # Сумма вознаграждения за рейсы. Если > 100 тариф2
        salary_variables = Variables.objects.filter(id__in=(1,2)).order_by('id')
        races_done = self.object.races_done
        races_salary = 0
        if races_done and races_done >= 100:
            races_salary = races_done * salary_variables[1].val
        elif races_done and races_done < 100:
            races_salary = float(races_done * salary_variables[0].val)
        context_data['races_salary'] = races_salary
        log.info("--- Standart: %s  Extra: %s Races: %s  Salary: %s" % (salary_variables[0].val, salary_variables[1].val, races_done, races_salary))
        # Суммарная зарплата
        context_data['total_salary'] = races_salary + accruals_sum
        # Остаток предыдущего месяца
        context_data['last_month_remains'] = SalaryFlow.objects.filter(year=self.report_prev_dt.year, month=self.report_prev_dt.month).aggregate(Sum('sum'))['sum__sum']
        # Начисления отчетного месяца
        context_data['report_month_accruals'] = SalaryFlow.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type__in=(1, 2, 3, 4, 5)).aggregate(Sum('sum'))['sum__sum']
        # Выданы авансы
        context_data['report_month_avances'] = SalaryFlow.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type__in=(6, 7)).aggregate(Sum('sum'))['sum__sum']

        # График - ходки по дням месяца
        races_by_day = Races.objects.filter(date_race__year=2016, date_race__month=7).extra({'dater':"day(date_race)"}).values('dater').annotate(count=Count('hodkis'))
        monthrange = calendar.monthrange(self.report_month_dt.year, self.report_month_dt.month)
        date_list = [x for x in range(1, monthrange[1]+1)]
        log.info("--- Month range: %s date list: %s" % (monthrange, date_list))
        for el in races_by_day:
            log.info("--- Day: %s sum: %s" % (el['dater'], el['count']))
        return context_data

    def get(self, request, *args, **kwargs):
        # получаем объект формы
        self.driver_pk = self.kwargs.get('driver_pk', None)
        self.object = self.get_object(self, *args, **kwargs)
        return self.render_to_response(self.get_context_data())