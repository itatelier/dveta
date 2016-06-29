# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *
from django.contrib.auth.decorators import login_required

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'refuels_rest', RefuelsFlowViewSet)



urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    url(r'^create/type/(?P<type_pk>\d+)/car/(?P<car_pk>\d+)/$', RefuelCreateView.as_view(), name='refuel_create'),
    # url(r'^(?P<pk>\d+)/card/$', CarCardView.as_view(), name='car_card'),
    # url(r'^(?P<pk>\d+)/driver/$', CarDriverView.as_view(), name='car_driver'),
    # url(r'^(?P<pk>\d+)/docs/$', CarDocsView.as_view(), name='car_docs'),
    # url(r'^(?P<pk>\d+)/update/$', CarUpdateView.as_view(), name='car_update'),
    url(r'^list/$', RefuelsListView.as_view(), name='refuels_list'),
    url(r'^check/cards/$', RefuelsCheckCardsView.as_view(), name='refuels_check_cards'),

]

