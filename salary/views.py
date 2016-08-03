# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *

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
        self.report_next_dt = report_month_firstday + timedelta(days=32)    # следующий месяц это первый день текущего + 32 дня
        return super(SalaryMonthSummaryView, self).dispatch(request, *args, **kwargs)


class SalaryMonthSummaryViewMech(SalaryMonthSummaryView):
    template_name = 'salary/salary_month_summary_mech.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryView, self).get_context_data(*args, **kwargs)
        # Получаем список сформированных зарплатных листов за указанный месяц
        log.info("--- Month: %s   Year: %s" %(self.report_month_dt.month, self.report_month_dt.year))
        summary_list = SalaryMonthSummary.objects.filter(month__exact=self.report_month_dt.month, year__exact=self.report_month_dt.year)
        context_data.update({
            'summary_list': summary_list
        })
        return context_data