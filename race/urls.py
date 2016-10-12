# -*- coding: utf8 -*

from django.conf.urls import url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'races_rest', RacesViewSet,)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^create/car/(?P<car_id>\d+)$', RaceCreateView.as_view(), name='race_create'),
    url(r'^(?P<pk>\d+)/update$', RaceUpdateView.as_view(), name='race_update'),
    url(r'^list/$', RacesListView.as_view(), name='races_list'),

]

