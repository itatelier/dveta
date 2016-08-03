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
    url(r'^month_summary/mechanic/$', SalaryMonthSummaryViewMech.as_view(), name='salary_month_summary_mech'),
]

