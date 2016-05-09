# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
#router = routers.DefaultRouter()
# router.register(r'cars_rest', CarsViewSet)


urlpatterns = [
    #
    # REST API
    # url(r'^api/', include(router.urls)),
    #
    url(r'^races/$', WdRacesView.as_view(), name='workday_races'),
]

