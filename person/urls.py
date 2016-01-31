# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *

base_path = 'company'

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'contacts_search_json', GetContactViewSet)


urlpatterns = patterns('',
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    # url(r'^get_contact_json/$', GetContactByPhoneJsonView.as_view(), name='contact_get_by_num_json'),
    # url(r'^get_contact_json/$', GetContactViewSet.as_view({'get': 'list'}), name='contact_get_by_num_json'),
    url(r'^create_company_contact_json/$', CreateCompanyContactJsonView.as_view(), name='company_contact_create_json'),
    url(r'^(?P<pk>\d+)/card/$', PersonCardView.as_view(), name='person_card'),

    # Employies
    url(r'^employee_create/$', EmployeeCreateView.as_view(), name='employee_create'),
    # url(r'^company_create_private/$', CompanyCreatePrivateView.as_view(), name='company_create_private'),
    # url(r'^(?P<pk>\d+)/edit/$', main_edit.as_view(), name=base_path + '_main_edit'),
    # url(r'^(?P<pk>\d+)/delete/$', main_delete.as_view(), name=base_path + '_main_delete'),
    # url(r'^list_clients/$', CompanyClientList.as_view(), name='company_list_clients'),
    # url(r'^main_list_json/$', main_list_json.as_view(), name=base_path + '_main_list_json'),
    # url(r'^(?P<pk>\d+)/card/employees$', main_card_employees.as_view(), name=base_path + '_main_card_employees'),
    # #
    # # Отделения
    # #
    # url(r'^(?P<company_pk>\d+)/branch_create/$', branch_create.as_view(), name=base_path + '_branch_create'),
    # url(r'^(?P<company_pk>\d+)/branch/(?P<pk>\d+)/card/$', branch_card.as_view(), name=base_path + '_branch_card'),
    # url(r'^(?P<company_pk>\d+)/branch/(?P<pk>\d+)/edit/$', branch_edit.as_view(), name=base_path + '_branch_edit'),
    # url(r'^branch/(?P<pk>\d+)/delete/$', branch_delete.as_view(), name=base_path + '_branch_delete'),
    # url(r'^branch_list/$', branch_list_index.as_view(), name=base_path + '_branch_list'),
    # url(r'^branch_list_json/$', branch_list_json.as_view(), name=base_path + '_branch_list_json'),
    # #
    # # Контрагенты
    # #
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

