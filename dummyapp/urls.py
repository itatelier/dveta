# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
from rest_framework import routers

base_path = 'company'

#REST
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = patterns('',
    url(r'^listing/$', DummyListingIndex.as_view(), name='dummy_listing'),
    url(r'^', include(router.urls)),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
)

