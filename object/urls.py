# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
# from phones.views import *


# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'objects_rest', ObjectsViewSet)
router.register(r'objects_rest_type_clients', ObjectsListingViewSet)


urlpatterns = patterns('',
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    url(r'^objects_list/$', ObjectListView.as_view(), name='objects_list'),
    url(r'^(?P<pk>\d+)/card/$', ObjectCardView.as_view(), name='object_card'),
    url(r'^company/(?P<company_pk>\d+)/object_create/$', ObjectCreateView.as_view(), name='object_create'),
    url(r'^company/(?P<company_pk>\d+)/(?P<pk>\d+)/update/$', ObjectUpdateView.as_view(), name='object_update'),
)

