# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *

base_path = 'company'

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'contragents_list', ContragentsViewSet)


urlpatterns = patterns('',
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    # url(r'^get_contact_json/$', GetContactByPhoneJsonView.as_view(), name='contact_get_by_num_json'),
    # url(r'^get_contact_json/$', GetContactViewSet.as_view({'get': 'list'}), name='contact_get_by_num_json'),
    #url(r'^create_company_ul/$', ContragentCompanyCreateULView.as_view(), name='company_contragent_create_ul'),

    # url(r'^(?P<company_pk>\d+)/contragent_create/$', contragent_create.as_view(), name=base_path + '_contragent_create'),
    # url(r'^(?P<company_pk>\d+)/contragent_ip_create/$', contragent_ip_create.as_view(), name=base_path + '_contragent_ip_create'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<pk>\d+)/card/$', contragent_card.as_view(), name=base_path + '_contragent_card'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', contragent_edit.as_view(), name=base_path + '_contragent_edit'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<pk>\d+)/delete/$', contragent_delete.as_view(), name=base_path + '_contragent_delete'),
    # url(r'^contragent_list/$', contragent_list_index.as_view(), name=base_path + '_contragent_list'),
    # url(r'^contragent_list_json/$', contragent_list_json.as_view(), name=base_path + '_contragent_list_json'),
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
)

