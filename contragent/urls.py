# -*- coding: utf8 -*

from django.conf.urls import url, include
from views import *
# from phones.views import *

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'contragents_list', ContragentsViewSet)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^contragents_list/$', ContragentsList.as_view(), name='contragents_list_all'),
    # #
    # # Банковские счета
    # #
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<contragent_pk>\d+)/create$', bank_account_create.as_view(), name=base_path + '_contragent_bank_create'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<contragent_pk>\d+)/bank/(?P<pk>\d+)/card', contragent_bank_card.as_view(), name=base_path + '_contragent_bank_card'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<contragent_pk>\d+)/bank/(?P<pk>\d+)/edit', contragent_bank_edit.as_view(), name=base_path + '_contragent_bank_edit'),
    # url(r'^bank_acc/(?P<pk>\d+)/delete', contragent_bank_delete.as_view(), name=base_path + '_contragent_bank_delete'),
    # #
    # # Телефоны
    # #
    # url(r'^phones_list/$', phones_list_index.as_view(), name=base_path + '_phones_list'),
    # url(r'^phones/', phones_list_json.as_view(), name=base_path + '_phones_list_json'),
    # url(r'^(?P<company_pk>\d+)/branch/(?P<branch_pk>\d+)/phones/edit$', branch_phones_manage.as_view(), name=base_path + '_branch_phones_manage'),
]

