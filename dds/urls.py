# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'dds_accounts_rest', AccountsViewSet,)
router.register(r'dds_flow_rest', DdsFlowViewSet,)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^account/refill/$', AccountRefillView.as_view(), name='dds_account_refill'),
    url(r'^flow/$', DdsFlowView.as_view(), name='dds_flow'),
    url(r'^operation/(?P<pk>\d+)/card/$', DdsOperationCard.as_view(), name='dds_operation_card'),
]