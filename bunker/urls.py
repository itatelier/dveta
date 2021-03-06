# -*- coding: utf8 -*

from django.conf.urls import url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'bunker_flow_rest', BunkerFlowViewSet,)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^api/bunker_remains/$', BunkerRemainsJSON.as_view(), name='bunker_remains'),
    url(r'^bunker_flow/$', BunkerFlowView.as_view(), name='bunker_flow'),
    url(r'^remains_report/$', BunkerFlowRemainsReportView.as_view(), name='bunker_remains_report'),
    url(r'^flow_add_op/$', BunkerOperationCreateView.as_view(), name='bunker_flow_add_op'),

]

