# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'dds_accounts_rest', AccountsViewSet,)
router.register(r'dds_flow_rest', DdsFlowViewSet,)
router.register(r'dds_items_rest', DdsItemsViewSet,)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #^(?P<pk>\d+)/delete/$
    url(r'^template/create$', DdsTemplateCreateView.as_view(), name='dds_template_create'),
    url(r'^template/(?P<pk>\d+)/delete/$', DdsTemplateDeleteView.as_view(), name='dds_template_delete'),
    url(r'^templates/group/(?P<group_id>\d+)/$', DdsTemplatesListView.as_view(), name='dds_templates_list'),
    url(r'^operation/template/(?P<template_id>\d+)/$', DdsTemplateOperation.as_view(), name='dds_template_operation'),
    url(r'^account_balance/$', AccountsBalanceView.as_view(), name='dds_accounts_balance'),
    url(r'^flow/$', DdsFlowView.as_view(), name='dds_flow'),
    url(r'^flow/account/(?P<account_id>\d+)/$', DdsFlowView.as_view(), name='dds_flow_by_account'),
    url(r'^operation/(?P<pk>\d+)/card/$', DdsOperationCard.as_view(), name='dds_operation_card'),
]