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

import logging
log = logging.getLogger('django')


class SalaryMonthSummaryView(TemplateView):
    template_name = 'salary/salary_month_summary.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryView, self).get_context_data(*args, **kwargs)
        # tqty = Sum(Func('remains', function='IFNULL', template='%(function)s(%(expressions)s,qty)'))

        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        log.info("--- Year: %s Month: %s" % (year, month))

        # Получаем список сформированных зарплатных листов за указанный месяц
        summary_list = SalaryMonthSummary.objects.filter(month__exact=month, year__exact=year)
        if summary_list:
            log.info("-- Summary rows: %s" % len(summary_list))

        context_data.update({
            # 'report_data': TalonsFlow.objects.filter(is_closed__isnull=True).exclude(operation_type__in=(1, 2)).values('employee_group',).annotate(remains=tqty)
            'summary_list': summary_list
            
        })
        return context_data


class SalaryMonthSummaryMechView(TemplateView):
    template_name = 'salary/salary_month_summary_mech.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(SalaryMonthSummaryMechView, self).get_context_data(*args, **kwargs)
        # tqty = Sum(Func('remains', function='IFNULL', template='%(function)s(%(expressions)s,qty)'))

        year = kwargs.get('year', None)
        month = kwargs.get('month', None)
        log.info("--- Year: %s Month: %s" % (year, month))

        # Получаем список сформированных зарплатных листов за указанный месяц
        summary_list = SalaryMonthSummary.objects.filter(month__exact=month, year__exact=year)
        if summary_list:
            log.info("-- Summary rows: %s" % len(summary_list))

        context_data.update({
            # 'report_data': TalonsFlow.objects.filter(is_closed__isnull=True).exclude(operation_type__in=(1, 2)).values('employee_group',).annotate(remains=tqty)
            'summary_list': summary_list

        })
        return context_data
