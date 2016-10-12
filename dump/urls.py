# -*- coding: utf8 -*

from django.conf.urls import url, include
from views import *
from django.contrib.auth.decorators import login_required

# REST
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'talons_rest', TalonsFlowViewSet)



urlpatterns = [
    #
    # REST API
    url(r'^api/', include(router.urls)),
    #
    # Persons
    url(r'^talons/move/buy/$', TalonsMoveBuyView.as_view(), name='talons_move_buy'),
    url(r'^talons/move/between/$', TalonsMoveBetweenView.as_view(), name='talons_move_between'),
    url(r'^talons_flow/$', TalonsFlowView.as_view(), name='talons_flow'),
    url(r'^talons/report/by_dump_group/$', TalonsReportRemainsByGroup.as_view(), name='talons_report_by_dump_group'),

]

