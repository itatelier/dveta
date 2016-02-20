# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
# router.register(r'bunker_flow_rest', BunkerFlowViewSet)


urlpatterns = patterns('',
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # url(r'^api/bunker_remains/$', BunkerRemainsJSON.as_view(), name='bunker_remains'),

)

