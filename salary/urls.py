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
    url(r'^month_summary/driver_stats/(?P<driver_pk>\d+)/$', SalaryMonthSummaryPersonalView.as_view(), name='salary_month_summary_personal'),
    url(r'^month_summary/refuels_by_car/(?P<car_pk>\d+)/$', SalaryMonthSummaryCarRefuelsView.as_view(), name='salary_month_summary_refuels_by_car'),
]

