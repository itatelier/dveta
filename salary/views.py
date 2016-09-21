# -*- coding: utf8 -*

from person.forms import *
from forms import *
from logic import *
# App spcific
from models import *
from company.models import *
from refuels.models import CarRunCheckFlow
from race.models import Races
from car.models import Cars
from common.models import Variables
from common.utils import *

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
        log.info("= Report period starts at: %s till end date:  %s" %(self.report_month_dt.date(), self.report_next_dt.date()))
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

    def get_context_data(self, *args, **kwargs):
        self.driver_pk = self.kwargs.get('driver_pk')
        context_data = super(SalaryMonthAnalyzeMechanicView, self).get_context_data(*args, **kwargs)
        context_data['driver'] = Employies.drivers.get(pk=self.driver_pk)
        # Список месячных показателей по каждой машине
        driver_stats = DriverStats(date_start=self.report_month_dt.date(), date_end=self.report_next_dt.date(), driver_pk=self.driver_pk)
        context_data['driver_month_stats'] = driver_stats.get_list()
        context_data['average_and_sum_stats'] = driver_stats.get_summary()
        # Сверки спидометра: количество
        context_data['stats_mech_checkups'] = CarRunCheckFlow.objects.filter(date__month=self.report_month_dt.month, date__year=self.report_month_dt.year, driver_id=self.driver_pk).count()
        context_data['accruals_list_penalties'] = SalaryFlow.objects.filter(employee=self.driver_pk, year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type=3).select_related('operation_type', 'operation_name')
        context_data['accruals_list_bonuses'] = SalaryFlow.objects.filter(employee=self.driver_pk, year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type=2).select_related('operation_type', 'operation_name')
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
        self.driver_pk = self.kwargs.get('driver_pk', None)
        # получаем объект формы
        self.object = self.get_object(self, *args, **kwargs)
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
                create_object.save()
            else:
                self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return "%s?year=%s&month=%s" % (reverse('salary_month_summary_mech'), self.report_month_dt.year, self.report_month_dt.month)


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
        driver_obj = Employies.drivers.get(pk=self.driver_pk)
        context_data['driver'] = driver_obj
        races_done = None
        final_salary = 0
        if hasattr(self.object, 'races_done'):
            # График - ходки по дням месяца
            races_by_day = Races.objects.filter(date_race__year=self.report_month_dt.year, date_race__month=self.report_month_dt.month)\
                .extra({'dater': "day(date_race)"}).values('dater')\
                .annotate(sum=Sum('hodkis'))
            monthrange = calendar.monthrange(self.report_month_dt.year, self.report_month_dt.month)
            date_list = [x for x in range(1, monthrange[1]+1)]
            races_graph_data = []
            for i in date_list:
                day_num = i
                day_count = 0
                for el in races_by_day:
                    if el['dater'] == day_num and el['sum'] > 0:
                        day_count = el['sum']
                races_graph_data.append(day_count)
            context_data['graph_days_list'] = date_list
            context_data['races_graph_data'] = races_graph_data
            # Занесенные данные о выполненных рейсах
            races_done = self.object.races_done
            # список начислений  Штрафы и премии
            context_data['accruals_list_penalty_and_bonus'] = SalaryFlow.objects.filter(
                operation_type__in=[2, 3],
                employee=self.driver_pk,
                year=self.report_month_dt.year,
                month=self.report_month_dt.month).select_related('operation_type')
            # Суммарные показатели начислений (group_by type)
            # список начислений авансы и зарплата
            context_data['accruals_list_other'] = SalaryFlow.objects.filter(
                operation_type__in=[1, 4, 5, 6, 7],
                employee=self.driver_pk,
                year=self.report_month_dt.year,
                month=self.report_month_dt.month).select_related('operation_type')
            # Суммарные показатели начислений (group_by type)
            context_data['accruals_summary'] = SalaryFlow.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type__in=(2, 3, 4, 5)).values_list('operation_type__type').annotate(total=Sum('sum'))
            accruals_sum = 0
            for el in context_data['accruals_summary']:
                accruals_sum += el[1]
            context_data['accruals_sum'] = accruals_sum
            final_salary += accruals_sum
            # Расчет оплаты за ходки
            races_tarif_stats = Races.objects.values('salary_tarif','salary_tarif__name', 'salary_tarif__plan_range', 'salary_tarif__standart_tarif', 'salary_tarif__overplan_tarif')\
                .filter(date_race__year=self.report_month_dt.year, date_race__month=self.report_month_dt.month, driver__pk=self.driver_pk)\
                .annotate(count_races=Count('salary_tarif'))
            races_salary_sum = 0
            for el in races_tarif_stats:
                if el['salary_tarif'] == 1:
                    el['sum'] = Races.objects.filter(driver=self.driver_pk, salary_tarif=1).aggregate(Sum('salary_driver_sum'))['salary_driver_sum__sum']
                    el['sort_index'] = 2
                    races_salary_sum += el['sum']
                else:
                    if el['count_races'] <= el['salary_tarif__plan_range']:
                        el['sum'] = el['count_races'] * el['salary_tarif__standart_tarif']
                        el['tarif_price'] = el['salary_tarif__standart_tarif']
                    elif el['count_races'] <= el['salary_tarif__plan_range']:
                        el['sum'] = el['count_races'] * el['salary_tarif__overplan_tarif']
                        el['tarif_price'] = el['salary_tarif__overplan_tarif']
                    el['sort_index'] = 1
                    races_salary_sum += el['sum']
            context_data['races_tarif_stats'] = sorted(races_tarif_stats, key=lambda item: item['sort_index'])  # Сортируем по значению sort_index
            context_data['races_salary_sum'] = races_salary_sum
            final_salary += races_salary_sum
            ### Вычеты и компенсации
            # Проживание на базе
            if driver_obj.report_baserent_in_period(self.report_month_dt, self.report_next_dt):
                basehouse_rent_sum = get_variable('salary_basehouse_rent')
                final_salary -= basehouse_rent_sum
                context_data['acr_basehouse_rent'] = basehouse_rent_sum
            # Налог НДФЛ
            if driver_obj.acr_ndfl_sum > 0:
                final_salary -= driver_obj.acr_ndfl_sum
                context_data['acr_ndfl_sum'] = driver_obj.acr_ndfl_sum
            # Компенсация мобильной связи
            if driver_obj.acr_mobile_compensation:
                mobile_comp_sum = get_variable('salary_mobile_comp')
                context_data['acr_mobile_compensation'] =  mobile_comp_sum
                final_salary += mobile_comp_sum
            # Итоговая зарплата
            context_data['final_salary'] = final_salary
            # Остаток предыдущего периода
            context_data['salary_prev_period_remains'] = SalaryFlow.objects.filter(year=self.report_prev_dt.year, month=self.report_prev_dt.month).aggregate(Sum('sum'))['sum__sum'] if not None else 0
            # Начисления отчетного месяца
            context_data['report_month_accruals'] = SalaryFlow.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type__in=(1, 2, 3, 4, 5), employee=self.driver_pk).aggregate(Sum('sum'))['sum__sum'] if not None else 0
            # Выданы авансы
            context_data['report_month_avances'] = SalaryFlow.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, operation_type__in=(6, 7), employee=self.driver_pk).aggregate(Sum('sum'))['sum__sum'] if not None else 0
            # Остаток на руки
            context_data['salary_now_remains'] = 0
            for item in ('salary_prev_period_remains', 'report_month_accruals', 'report_month_avances'):
                if context_data[item] is not None:
                    context_data['salary_now_remains'] += context_data[item]
                else:
                    context_data[item] = 0
        else:
            pass
        return context_data

    def get(self, request, *args, **kwargs):
        # получаем объект формы
        self.driver_pk = self.kwargs.get('driver_pk', None)
        self.object = self.get_object(self, *args, **kwargs)
        return self.render_to_response(self.get_context_data())


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
        context_data['summary_list'] = SalaryMonthSummary.objects.filter(year=self.report_month_dt.year, month=self.report_month_dt.month, check_status__in=(2, 3))
        return context_data


