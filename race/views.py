# -*- coding: utf8 -*

from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import TemplateView
from django.forms.models import modelform_factory
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
from common.utils import GetObjectOrNone
from django.shortcuts import get_object_or_404
from common.forms import *


from models import *
# from phones.models import *
from person.forms import *
from forms import *
from contragent.models import *
from rest_framework import viewsets, generics, filters
from django.http import HttpResponseRedirect


class RaceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'race/race_create.html'
    form_class = RaceCreateForm
    model = Races

    def get_success_url(self):
        return reverse('car_card', args=(self.object.id,))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            race_object = form.save(commit=False)
            race_object.save()
            self.success_url = '/races/%s/card' % race_object.id
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))