# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from bunker.models import BunkerFlow
from object.models import ObjectTypes
from forms import *
from common.utils import DateTimeNowToSql


# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonPost
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.db.models import Sum, Count, Func, F
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from common.utils import DateNowInput




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
    card_pk = False
    later_add = False

    # def dispatch(self, request, *args, **kwargs):
    #     self.car_pk = self.kwargs.get('car_pk', False)
    #     self.type_pk = self.kwargs.get('type_pk', False)
    #     self.driver_pk = self.request.GET.get('driver_pk', False)
    #     self.card_pk = self.request.GET.get('card_pk', False)
    #     self.later_add = self.request.GET.get('later_add', False)
    #     return super(RefuelCreateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(RefuelCreateView, self).get_form_kwargs()
        car_object =  Cars.objects.select_related('model').get(pk=self.kwargs.get('car_pk'))
        update_params = {
            'car': self.kwargs.get('car_pk', None),
            'type': self.kwargs.get('type_pk', None),
            'driver': self.request.GET.get('driver_pk', None),
            'later_add': self.request.GET.get('later_add', None),
        }
        if update_params['type'] and int(update_params['type']) == 0:
            log.info('--- Update param fuel_card num=%s' % car_object.fuel_card.pk)
            update_params['fuel_card'] = car_object.fuel_card.pk
        kwargs.update(update_params)
        return kwargs
    #
    # def get(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     self.object = None
    #     # Передача параметров в форму из урла
    #     initial = {}
    #     data = {'type_pk': self.type_pk}    # Данные для контекста шаблона
    #     if self.car_pk:
    #         initial['car'] = self.car_pk
    #         form.fields['car'].widget = widgets.HiddenInput()
    #         data['car'] = Cars.objects.select_related('model').get(pk=self.car_pk)
    #         # Если заправка по карте
    #         if int(self.type_pk) == 0:
    #             initial['fuel_card'] = data['car'].fuel_card.pk
    #     if self.driver_pk:
    #         initial['driver'] = self.driver_pk
    #         form.fields['driver'].widget = widgets.HiddenInput()
    #         data['driver'] = Employies.drivers.get(pk=self.driver_pk)
    #     if self.card_pk:
    #         data['card'] = FuelCards.objects.select_related('fuel_company').get(pk=self.card_pk)
    #     # Если тип заправки "по карте", то сумма не указывается и будет при сохранении формы рассчитана из справочника цен на топливо (FuelTypes)
    #     if int(self.type_pk) == 0:
    #         form.fields['sum'].widget = widgets.HiddenInput()
    #     # Если заправка добавляется задним числом
    #     log.info("--- Later add: %s" % self.later_add)
    #
    #     if int(self.later_add) == 1:
    #         # form.fields['date_refuel'] = DateInput()
    #         form.fields['date_refuel'].widget = RuDateWidget()
    #         initial['date_refuel'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    #     else:
    #         initial['date_refuel'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    #     form.initial = initial
    #     return self.render_to_response(self.get_context_data(form=form, data=data))

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return '/'

    def get_context_data(self, *args, **kwargs):
        context_data = super(RefuelCreateView, self).get_context_data(*args, **kwargs)
        context_data['refuels'] = RefuelsFlow.objects.list_with_run_checks(car_id=self.kwargs.get('car_pk'), limit=10)
        type_pk = self.kwargs.get('type_pk', None)
        car_pk = self.kwargs.get('car_pk', False)
        card_pk = self.request.GET.get('card_pk', False)
        driver_pk = self.request.GET.get('driver_pk', False)
        if car_pk:
            context_data['car'] =  Cars.objects.select_related('model').get(pk=car_pk)
        if type_pk and int(type_pk) == 0:
            context_data['card'] = FuelCards.objects.select_related('fuel_company').get(assigned_to_car=car_pk)
        if driver_pk:
            context_data['driver'] = Employies.drivers.get(pk=driver_pk)

        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if int(self.type_pk) == 0:
            form.fields['sum'].required = False
            form.fields['sum'].widget = widgets.HiddenInput()
        if form.is_valid():
            refuel_object = form.save(commit=False)
        # Если тип заправки "По карте" - присваиваем карты привязанную к машине
        # сумма не указываетя, но получается из текущей стоимости топлива
            if int(self.type_pk) == 0:
                # Получаем цену топлива
                fuel_type_object = FuelTypes.objects.get(pk=1)
                refuel_object.sum = fuel_type_object.price * form.cleaned_data['amount']
                if int(self.card_pk):
                    refuel_object.fuel_card = FuelCards(pk=self.card_pk)
                else:
                    refuel_object.fuel_card = Cars.objects.get(pk=self.car_pk).fuel_card
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
            log.info("--- Later POST add: %s" % self.later_add)

            if int(self.later_add) == 1:
                form.fields['date_refuel'].widget = RuDateWidget()
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form, data=data))


class RunCheckCreateView(LoginRequiredMixin, CreateView):
    template_name = 'refuels/run_check_create.html'
    form_class = RunCheckForm
    object = None
    model = CarRunCheckFlow
    car_pk = False
    driver_pk = False

    def dispatch(self, request, *args, **kwargs):
        self.car_pk = self.kwargs.get('car_pk', False)
        self.driver_pk = self.request.GET.get('driver_pk', False)
        return super(RunCheckCreateView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = None
        initial = {}
        data = {}   # Данные для контекста шаблона
        if self.car_pk:
            initial['car'] = self.car_pk
            form.fields['car'].widget = widgets.HiddenInput()
            data['car'] = Cars.objects.select_related('model').get(pk=self.car_pk)
        if self.driver_pk:
            initial['driver'] = self.driver_pk
            form.fields['driver'].widget = widgets.HiddenInput()
            data['driver'] = Employies.drivers.get(pk=self.driver_pk)
        form.initial = initial
        return self.render_to_response(self.get_context_data(form=form, data=data))

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return '/'

    def get_context_data(self, *args, **kwargs):
        context_data = super(RunCheckCreateView, self).get_context_data(*args, **kwargs)
        context_data['refuels'] = RefuelsFlow.objects.list_with_run_checks(car_id=self.car_pk, limit=10)
        return context_data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            object = form.save(commit=False)
            object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            data = {}    # Данные для контекста шаблона
            if self.car_pk:
                form.fields['car'].widget = widgets.HiddenInput()
                data['car'] = Cars.objects.select_related('model').get(pk=self.car_pk)
            if self.driver_pk:
                form.fields['driver'].widget = widgets.HiddenInput()
                data['driver'] = Employies.drivers.get(pk=self.driver_pk)
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


class RefuelsCheckReportView(LoginRequiredMixin, TemplateView):
    template_name = 'refuels/refuels_check_report.html'
    report_month_dt = False
    report_prev_dt = False
    report_next_dt = False

    def dispatch(self, request, *args, **kwargs):
        # Месяц и год отчета будет предыдущий от даты "сегодня" или даты из запроса
        today = datetime.now()
        first_month_day = today.replace(day=1) # прошлый месяц это 1е исло текщуго минус 1 день
        self.report_month_dt = first_month_day - timedelta(days=1)
        if request.GET.get('month') and request.GET.get('year'):
            try:
                self.report_month_dt = datetime.strptime("1/%s/%s" % (request.GET.get('month'), request.GET.get('year')), "%d/%m/%Y")
            except ValueError as err:
                log.info("- Month and Year params not good!")
        report_month_firstday = self.report_month_dt.replace(day=1)
        self.report_prev_dt = report_month_firstday - timedelta(days=1)
        self.report_next_dt = report_month_firstday + timedelta(days=32) # следующий месяц это первый день текущего + 32 дня
        return super(RefuelsCheckReportView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context_data = super(RefuelsCheckReportView, self).get_context_data(*args, **kwargs)
        nowtime = datetime.now()
        last_month_num = nowtime.month - 1
        # Подготовка запроса
        not_checked = Sum(Func('checked', function='IF', template='%(function)s(%(expressions)s=0, 1, 0)'))
        already_checked = Sum(Func('checked', function='IF', template='%(function)s(%(expressions)s=0, 0, 1)'))
        check_finished = Func(
                not_checked,
                function='IF', template='%(function)s(%(expressions)s=0, 1, 0)'
        )
        context_data['refuels'] = RefuelsFlow.objects.filter(
                type=0,
                date_refuel__year=self.report_month_dt.year,
                date_refuel__month=self.report_month_dt.month,
            ).values('car__nick_name', 'car__pk','fuel_card__num', 'fuel_card__pk', 'fuel_card__fuel_company__name').annotate(
            total_amount=Sum('amount'),
            total_refuels = Count('id'),
            already_checked=already_checked,
            not_checked=not_checked,
            check_finished=check_finished
        )
        context_data['prev_month'] = last_month_num - 1
        context_data['next_month'] = last_month_num - 1
        return context_data


class RefuelsCheckListView(LoginRequiredMixin, TemplateView):
    template_name = 'refuels/refuels_check_operations.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(RefuelsCheckListView, self).get_context_data(*args, **kwargs)
        car_pk = kwargs.get('car_pk')
        fuel_card_pk = kwargs.get('fuel_card_pk')
        month = kwargs.get('month')
        year = kwargs.get('year')
        refuels = RefuelsFlow.objects.filter(
            type=0,
            date_refuel__year=year,
            date_refuel__month=month,
            car__pk=car_pk,
            fuel_card__pk=fuel_card_pk
        )
        context_data['refuels'] = refuels
        report_dt = datetime.strptime("1/%s/%s" % (month, year), "%d/%m/%Y")
        context_data['report_dt'] = report_dt
        context_data['report_date_my'] = report_dt.strftime("%B %Y")

        context_data['car'] = Cars.objects.get(pk=car_pk)
        context_data['card'] = FuelCards.objects.get(pk=fuel_card_pk)
        return context_data


class UpdateCheckedRefuelsAjax(JsonPost):
    required_params = ['selected_ops',]

    def update_data(self, request):
        selected_ops = request.POST.getlist('selected_ops[]')
        unselected_ops = request.POST.getlist('unselected_ops[]')
        self.json['selected_ops'] = selected_ops
        self.json['unselected_ops'] = unselected_ops
        RefuelsFlow.objects.filter(checked=False, pk__in=selected_ops).update(checked=True)
        RefuelsFlow.objects.filter(checked=True, pk__in=unselected_ops).update(checked=False)

