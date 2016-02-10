# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
# router.register(r'contacts_search_json', GetContactViewSet)
# router.register(r'employies_rest', EployiesViewSet)


urlpatterns = patterns('',
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    url(r'^create/$', CarCreateView.as_view(), name='car_create'),
    url(r'^(?P<pk>\d+)/card/$', CarCardView.as_view(), name='car_card'),
    url(r'^(?P<pk>\d+)/update/$', CarUpdateView.as_view(), name='car_update'),
    # url(r'^(?P<pk>\d+)/contacts/$', PersonContactsUpdateView.as_view(), name='person_contacts_update'),
)

