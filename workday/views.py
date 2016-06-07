# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone
from django.shortcuts import get_object_or_404
from common.forms import *
from race.models import *


class WdRacesView(LoginRequiredMixin, TemplateView):
    template_name = 'workday/workday_races2.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(WdRacesView, self).get_context_data(*args, **kwargs)
        context_data['races'] = Races.objects.select_related('object', 'dump', 'company', 'race_type', 'cargo_type', 'bunker_type')
        # context_data['company'] = Companies.objects.get(pk=company_pk)
        # context_data['bunker_types_summ'] = ('type1_summ', 'type2_summ', 'type3_summ', 'type4_summ', 'type5_summ', 'type6_summ', 'type7_summ', )
        return context_data