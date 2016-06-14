# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone
from django.shortcuts import get_object_or_404
from common.forms import *
from datetime import datetime
from race.models import *
from dds.models import *
from person.models import Employies


class WorkdayBaseView(LoginRequiredMixin, TemplateView):
    driver_pk = False
    date = False

    def dispatch(self, request, *args, **kwargs):
        self.driver_pk = self.kwargs.get('driver_pk', False)
        self.date = datetime.strptime(self.kwargs.get('date', False), '%d-%m-%y')
        return super(WorkdayBaseView, self).dispatch(request, *args, **kwargs)

    def driver(self):
        return Employies.objects.get(pk=self.driver_pk)


class WorkdayRacesView(WorkdayBaseView):
    template_name = 'workday/workday_races.html'

    def races(self):
        log.info("--- DAte: %s" % self.date.isoformat())
        return Races.objects.filter(
            driver=self.driver_pk,
            date_race__day=self.date.day,
            date_race__month=self.date.month,
            date_race__year=self.date.year,
        ).select_related('object', 'dump', 'company', 'race_type', 'cargo_type', 'bunker_type')


class WorkdayDdsView(WorkdayBaseView):
    template_name = 'workday/workday_dds.html'

    def dds_flow(self):
        driver_pk = self.kwargs.get('driver_pk')
        return DdsFlow.objects.filter(account__employee__pk=driver_pk)


