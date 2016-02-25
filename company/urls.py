# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
from contragent.views import *
from object.views import ClientObjectsView
# from phones.views import *

base_path = 'company'

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'clients', CompanyClientsViewSet)
router.register(r'company_contacts', CompanyContactsViewSet)


urlpatterns = patterns('',
    #
    # #  REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^company_create/$', CompanyCreateFirmView.as_view(), name='company_create_firm'),
    url(r'^company_create_private/$', CompanyCreatePrivateView.as_view(), name='company_create_private'),
    url(r'^(?P<pk>\d+)/card/$', CompanyClientCardView.as_view(), name='company_card_client'),
    url(r'^(?P<pk>\d+)/update/$', CompanyUpdateInfoView.as_view(), name='company_update_info'),
    url(r'^(?P<pk>\d+)/delete/$', CompanyDelete.as_view(), name='company_delete'),
    url(r'^(?P<pk>\d+)/contacts/$', CompanyContactsView.as_view(), name='company_contacts'),
    url(r'^(?P<company_pk>\d+)/contacts/(?P<pk>\d+)/update/$', CompanyContactUpdateView.as_view(), name='company_contacts_update'),
    url(r'^list_clients/$', CompanyClientList.as_view(), name='company_list_clients'),
    url(r'^search_contacts/$', CompanyContactSearchView.as_view(), name='company_search_contacts'),
    url(r'^(?P<company_pk>\d+)/client_options', ClientOptionsUpdateView.as_view(), name='company_client_options'),
    # #
    # # Отделения
    # #
    url(r'^(?P<company_pk>\d+)/branch_create/$', BranchCreateView.as_view(), name='company_branch_create'),
    url(r'^(?P<company_pk>\d+)/branch/(?P<pk>\d+)/card/$', BranchCardView.as_view(), name='company_branch_card'),
    url(r'^(?P<company_pk>\d+)/branch/(?P<pk>\d+)/edit/$', BranchUpdateView.as_view(), name='company_branch_update'),
    url(r'^(?P<company_pk>\d+)/branch/(?P<pk>\d+)/delete/$', BranchDelete.as_view(), name='company_branch_delete'),
    # #
    # # Контрагенты
    # #
    url(r'^(?P<company_pk>\d+)/contragent_create_ul/$', ContragentCompanyCreateULView.as_view(), name='company_contragent_create_ul'),
    url(r'^(?P<company_pk>\d+)/contragent_create_ip/$', ContragentCompanyCreateIPView.as_view(), name='company_contragent_create_ip'),
    url(r'^(?P<company_pk>\d+)/contragent/(?P<pk>\d+)/type/(?P<type>\d+)/edit/$', ContragentCompanyUpdateView.as_view(), name='company_contragent_update'),
    # #
    # # Объекты
    # #
    url(r'^(?P<company_pk>\d+)/objects/$', ClientObjectsView.as_view(), name='company_objects'),
    # #
    # # Банковские счета
    # #
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<contragent_pk>\d+)/create$', bank_account_create.as_view(), name=base_path + '_contragent_bank_create'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<contragent_pk>\d+)/bank/(?P<pk>\d+)/card', contragent_bank_card.as_view(), name=base_path + '_contragent_bank_card'),
    # url(r'^(?P<company_pk>\d+)/contragent/(?P<contragent_pk>\d+)/bank/(?P<pk>\d+)/edit', contragent_bank_edit.as_view(), name=base_path + '_contragent_bank_edit'),
    # url(r'^bank_acc/(?P<pk>\d+)/delete', contragent_bank_delete.as_view(), name=base_path + '_contragent_bank_delete'),
)

