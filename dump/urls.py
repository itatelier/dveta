# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
from django.contrib.auth.decorators import login_required

# REST
from rest_framework import routers
router = routers.DefaultRouter()
# router.register(r'refuels_rest', RefuelsFlowViewSet)



urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    url(r'^price/add/$', DumpPriceAddView.as_view(), name='dump_price_add'),
]

