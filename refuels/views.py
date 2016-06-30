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
from django.db.models import Sum, Count, Func, F
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
    car_pk = False
    type_pk = False
    driver_pk = False

    def dispatch(self, request, *args, **kwargs):
        self.car_pk = self.kwargs.get('car_pk', False)
        self.type_pk = self.kwargs.get('type_pk', False)
        self.driver_pk = self.request.GET.get('driver_pk', False)
        return super(RefuelCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        # Передача параметров в форму из урла
        initial = {}
        data = {}    # Данные для контекста шаблона
        initial['type'] = self.type_pk
        if self.car_pk:
            initial['car'] = self.car_pk
            form.fields['car'].widget = widgets.HiddenInput()
            data['car'] = Cars.objects.select_related('model').get(pk=self.car_pk)
        if self.driver_pk:
            initial['driver'] = self.driver_pk
            form.fields['driver'].widget = widgets.HiddenInput()
            data['driver'] = Employies.drivers.get(pk=self.driver_pk)
        if not int(self.type_pk) == 0:
            form.fields['fuel_card'].widget = widgets.HiddenInput()
        form.initial = initial
        return self.render_to_response(self.get_context_data(form=form, data=data))

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return reverse('/')

    def get_context_data(self, *args, **kwargs):
        context_data = super(RefuelCreateView, self).get_context_data(*args, **kwargs)
        context_data['refuels'] = RefuelsFlow.objects.filter(car__pk=self.car_pk).order_by('-date')[:10]
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            refuel_object = form.save(commit=False)
            # Если тип заправки "По карте" - присваиваем карты привязанную к машине
            if int(self.type_pk) == 0:
                refuel_object.fuel_card = FuelCards.objects.get(assigned_car__pk=self.car_pk)
            refuel_object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            data = {}    # Данные для контекста шаблона
            if self.car_pk:
                form.fields['car'].widget = widgets.HiddenInput()
                data['car'] = Cars.objects.select_related('model').get(pk=self.car_pk)
            if self.driver_pk:
                form.fields['driver'].widget = widgets.HiddenInput()
                data['driver'] = Employies.drivers.get(pk=self.driver_pk)
            if not int(self.type_pk) == 0:
                form.fields['fuel_card'].widget = widgets.HiddenInput()
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form, data=data))


class RefuelsFlowViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = RefuelsFlow.objects.select_related(
        'car',
        'fuel_card',
        'driver',
    ).prefetch_related('driver__person', 'fuel_card__fuel_company', 'driver__status')
    serializer_class = RefuelsFlowSerializer
    search_fields = ('comment', )
    filter_class = RefuelsFlowFilters
    ordering_fields = ('car', 'driver__nick', 'fuelcard', )


class RefuelsListView(LoginRequiredMixin, TemplateView):
    template_name = 'refuels/list_refuels.html'


class RefuelsCheckCardsView(LoginRequiredMixin, TemplateView):
    template_name = 'refuels/refuels_check_fuelcards.html'
    report_month_dt = False
    report_prev_dt = False
    report_next_dt = False

    def dispatch(self, request, *args, **kwargs):
        today = datetime.now()
        first_month_day = today.replace(day=1)
        self.report_month_dt = first_month_day - timedelta(days=1)
        report_month_firstday = self.report_month_dt.replace(day=1)
        self.report_prev_dt = report_month_firstday - timedelta(days=1)
        self.report_next_dt = report_month_firstday + timedelta(days=32)
        return super(RefuelsCheckCardsView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super(RefuelsCheckCardsView, self).get_context_data(*args, **kwargs)
        nowtime = datetime.now()
        last_month_num = nowtime.month - 1
        # Подготовка запроса
        not_checked = Sum(Func('checked', function='IF', template='%(function)s(%(expressions)s=0, 1, 0)'))
        already_checked = Sum(Func('checked', function='IF', template='%(function)s(%(expressions)s=0, 0, 1)'))
        check_finished = Func(
                not_checked,
                function='IF', template='%(function)s(%(expressions)s=0, 1, 0)'
        )
        context_data['refuels'] = RefuelsFlow.objects.values('car__nick_name', 'car__pk').annotate(
            total_amount=Sum('amount'),
            total_refuels = Count('id'),
            already_checked=already_checked,
            not_checked=not_checked,
            check_finished=check_finished
        )
        context_data['prev_month'] = last_month_num - 1
        context_data['next_month'] = last_month_num - 1
        return context_data
