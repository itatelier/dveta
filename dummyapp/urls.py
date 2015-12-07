# -*- coding: utf8 -*

from django.conf.urls import patterns, url, include
from views import *
from rest_framework import routers

base_path = 'company'

# REST
router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)

urlpatterns = patterns('',
    url(r'^listing/$', DummyListingIndex.as_view(), name='dummy_listing'),
    url(r'^api/', include(router.urls)),
)

