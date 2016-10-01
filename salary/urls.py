# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *


# REST
from rest_framework import routers
#router = routers.DefaultRouter()
# router.register(r'cars_rest', CarsViewSet)


urlpatterns = [
    #
    # REST API
    # url(r'^api/', include(router.urls)),
    #
    # url(r'^year/(?P<year>\d{4})/month/(?P<month>\d{2})/$', SalaryMonthSummaryView.as_view(), name='salary_month_summary'),
    url(r'^month_summary/report/mechanic/$', SalaryMonthSummaryViewMech.as_view(), name='salary_month_summary_mech'),
    url(r'^month_summary/report/office/$', SalaryMonthSummaryViewOffice.as_view(), name='salary_month_summary_office'),
    url(r'^month_summary/analyze_mech/driver/(?P<driver_pk>\d+)/$', SalaryMonthAnalyzeMechanicView.as_view(), name='salary_month_analyze_mechanic'),
    url(r'^month_summary/analyze_office/driver/(?P<driver_pk>\d+)/$', SalaryMonthAnalyzeOfficeView.as_view(), name='salary_month_analyze_office'),
    url(r'^month_summary/analyze_top/driver/(?P<driver_pk>\d+)/$', SalaryMonthAnalyzeTopView.as_view(), name='salary_month_analyze_top'),
    url(r'^month_summary/refuels_by_car/driver/(?P<car_pk>\d+)/$', SalaryMonthSummaryCarRefuelsView.as_view(), name='salary_month_summary_refuels_by_car'),
    url(r'^salary_flow/operation_create/year/(?P<year>\d{4})/month/(?P<month>\d{1,2})/type/(?P<type_pk>\d+)/employee/(?P<employee_pk>\d+)/$', SalaryOperationCreateView.as_view(), name='salary_operation_create'),
]

