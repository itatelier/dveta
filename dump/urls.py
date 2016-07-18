# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
from django.contrib.auth.decorators import login_required

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'talons_rest', TalonsFlowViewSet)



urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    url(r'^price/add/$', TalonsMoveBuyView.as_view(), name='talons_move_buy'),
]

