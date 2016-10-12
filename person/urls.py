# -*- coding: utf8 -*

from django.conf.urls import url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'contacts_search_json', GetContactViewSet)
router.register(r'employies_rest', EployiesViewSet)


urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    # url(r'^get_contact_json/$', GetContactByPhoneJsonView.as_view(), name='contact_get_by_num_json'),
    # url(r'^get_contact_json/$', GetContactViewSet.as_view({'get': 'list'}), name='contact_get_by_num_json'),
    # url(r'^create_company_contact_json/$', CreateCompanyContactJsonView.as_view(), name='company_contact_create_json'),
    url(r'^(?P<pk>\d+)/card/$', PersonCardView.as_view(), name='person_card'),
    url(r'^(?P<pk>\d+)/update/$', PersonUpdateView.as_view(), name='person_update'),
    url(r'^(?P<pk>\d+)/contacts/$', PersonContactsUpdateView.as_view(), name='person_contacts_update'),
    url(r'^(?P<person_pk>\d+)/contacts/(?P<pk>\d+)/delete/$', ContactDeleteView.as_view(), name='contact_delete'),
    url(r'^(?P<person_pk>\d+)/contacts/setmain/ajax/$', ContactSetMainView.as_view(), name='contact_set_main'),

    # Employies
    url(r'^employee/(?P<pk>\d+)/card/$', EmployeeCardView.as_view(), name='employee_card'),
    url(r'^employee/(?P<pk>\d+)/salary/settings$', EmployeeUpdateSalaryView.as_view(), name='employee_salary_settings'),
    url(r'^employee_create/$', EmployeeCreateView.as_view(), name='employee_create'),
    url(r'^employies_list/$', EmployiesListView.as_view(), name='employies_list'),


]

