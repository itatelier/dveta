# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
# router.register(r'races_rest', RacesViewSet,)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^account/refill/$', AccountRefillView.as_view(), name='dds_account_refill'),

]