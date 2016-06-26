# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from bunker.models import BunkerFlow
from object.models import ObjectTypes
from forms import *
from common.utils import DateTimeNowToSql


# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta



# API
from serializers import *
from person.serializers import *
from rest_framework import viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status


class RefuelCreateView(LoginRequiredMixin, CreateView):
    template_name = 'refuels/refuel_create_update.html'
    form_class = RefuelForm
    model = RefuelsFlow
    driver_pk = False

    def dispatch(self, request, *args, **kwargs):
        self.driver_pk = self.kwargs.get('driver_pk', False)
        return super(RefuelCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        # Передача параметров в форму из урла
        initial = {}
        data = {}    # Данные для контекста шаблона
        if self.driver_pk:
            initial['driver'] = self.driver_pk
            form.fields['driver'].widget = widgets.HiddenInput()
            data['driver'] = Employies.drivers.get(pk=self.driver_pk)
        if self.request.GET.get('car_id'):
            car_id = self.request.GET.get('car_id')
            initial['car'] = car_id
            form.fields['car'].widget = widgets.HiddenInput()
            data['car'] = Cars.objects.get(pk=car_id)

        form.initial = initial
        return self.render_to_response(self.get_context_data(form=form, data=data))

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return reverse('/')

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         # Создаем клон авто в "Объектах"
    #         car_nick_name = u'Авто %s' % form.cleaned_data.get("nick_name")
    #         object_type_object = ObjectTypes.objects.get(pk=2)
    #         car_object = Objects.objects.create(name=car_nick_name, type=object_type_object)
    #         # Создаем пустую запись в Car Documents
    #         docs_object = CarDocs(date_update=DateTimeNowToSql())
    #         docs_object.save()
    #         create_object = form.save(commit=False)
    #         create_object.car_object = car_object
    #         create_object.docs = docs_object
    #         create_object.status = CarStatuses(pk=1)
    #         create_object.save()
    #         self.success_url = '/cars/%s/card' % create_object.id
    #         return HttpResponseRedirect(self.success_url)
    #     else:
    #         self.object = form.instance
    #         return self.render_to_response(self.get_context_data(form=form))
