# -*- coding: utf8 -*

from django.conf.urls import url, include
from views import *
from django.contrib.auth import views as auth_views
import debug_toolbar
# from phones.views import *
from django.conf import settings


# REST
from rest_framework import routers
#router = routers.DefaultRouter()
# router.register(r'cars_rest', CarsViewSet)


urlpatterns = [
    #
    url(r'^accounts/login/$', auth_views.login, {'login': 'registration/login.html'}),
    # REST API
    # url(r'^api/', include(router.urls)),
    #
    url(r'^(?P<date>\d{1,2}-\d{1,2}-\d{2})/car/(?P<car_pk>\d+)/races/$', WorkdayRacesView.as_view(), name='workday_races'),
    url(r'^(?P<date>\d{1,2}-\d{1,2}-\d{2})/car/(?P<car_pk>\d+)/dds/$', WorkdayDdsView.as_view(), name='workday_dds'),
    url(r'^(?P<date>\d{1,2}-\d{1,2}-\d{2})/car/(?P<car_pk>\d+)/refuels/$', WorkdayRefuelsView.as_view(), name='workday_refuels'),
    url(r'^(?P<date>\d{1,2}-\d{1,2}-\d{2})/car/(?P<car_pk>\d+)/talons/$', WorkdayTalonsView.as_view(), name='workday_talons'),
    url(r'^__debug__/', include(debug_toolbar.urls))
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += urlpatterns[url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]