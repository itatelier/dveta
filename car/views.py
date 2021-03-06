# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from bunker.models import BunkerFlow
from object.models import ObjectTypes
from forms import *
from common.utils import DateTimeNowToSql
from django.core.exceptions import ObjectDoesNotExist
from common.view_tools import CreateUpdateView

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.db.models import Sum
from django.shortcuts import get_object_or_404


# API
from serializers import *
from person.serializers import *
from rest_framework import viewsets, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status


class CarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'car/car_create_update.html'
    form_class = CarCreateWithoutComment
    model = Cars

    def get_success_url(self):
        return reverse('car_card', args=(self.object.id,))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Создаем клон авто в "Объектах"
            car_nick_name = u'Авто %s' % form.cleaned_data.get("nick_name")
            object_type_object = ObjectTypes.objects.get(pk=2)
            car_object = Objects.objects.create(name=car_nick_name, type=object_type_object)
            # Создаем пустую запись в Car Documents
            docs_object = CarDocs(date_update=DateTimeNowToSql())
            docs_object.save()
            create_object = form.save(commit=False)
            create_object.car_object = car_object
            create_object.docs = docs_object
            create_object.status = CarStatuses(pk=1)
            create_object.save()
            self.success_url = '/cars/%s/card' % create_object.id
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class CarCardView(LoginRequiredMixin, DetailView):
    template_name = "car/car_card.html"
    model = Cars
    queryset = Cars.objects.select_related('model', 'model__brand', 'fuel_type', 'load_type', 'unit_group', 'car_object', 'mechanic', 'mechanic__person', 'driver')

    def get_context_data(self, *args, **kwargs):
        context_data = super(CarCardView, self).get_context_data(*args, **kwargs)
        context_data['bunkers_onboard'] = self.object.car_object.bunker_remain.all()
        context_data['docs'] = Cars.get_docs(self, car_pk=self.kwargs.get('pk', None))
        # context_data['bunkers_onboard'] = BunkerFlow.remains.by_object_id(self.object.car_object_id)
        # context_data['bunkers_onboard'] = BunkerFlow.objects.filter(object__pk=self.object.car_object.id).aggregate(Sum('qty'))
        return context_data


class CarUpdateView(LoginRequiredMixin, UpdateView):
        template_name = "car/car_create_update.html"
        model = Cars
        form_class = CarCreateForm

        def get_success_url(self):
            return reverse('car_card', args=(self.object.id,))


class CarsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # queryset = Cars.objects.all()
    queryset = Cars.objects.filter()\
        .select_related('model', 'model__brand', 'fuel_type', 'load_type', 'unit_group', 'car_object', 'status', 'driver', 'driver__person', 'mechanic', 'mechanic__person')
        # prefetch_related( 'mechanic', 'mechanic__person', 'mechanic__type', 'mechanic__role', 'mechanic__status', 'driver', 'driver__person', 'driver__type', 'driver__role', 'driver__status')

    # queryset = Cars.objects.filter().select_related('model', 'model__brand', 'fuel_type', 'unit_group', 'car_object',
    #                                                 'status', 'mechanic', 'mechanic__person', 'mechanic__type', 'mechanic__role', 'mechanic__status',
    #                                                 'driver', 'driver__person')
    serializer_class = CarsSerizlizer
    filter_class = CarFilters
    search_fields = ('reg_num', 'nick_name', 'comment', )
    ordering_fields = ('model', 'fuel_type', 'mechanic', 'unit_group', 'reg_num', 'nick_name', 'trailer_attached', 'date_add', 'status')


class CarListView(LoginRequiredMixin, TemplateView):
    template_name = "car/list_cars.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(CarListView, self).get_context_data(*args, **kwargs)
        context_data['mechanics'] = Employies.mechanics.select_related('person')
        return context_data


class CarDriverView(LoginRequiredMixin, UpdateView):
    template_name = "car/car_driver.html"
    model = Cars
    form_class = CarDriverUpdateForm

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return reverse('car_card', args=(self.object.id,))


class CarFuelCardView(LoginRequiredMixin, UpdateView):
    template_name = "car/car_fuel_card.html"
    model = Cars
    form_class = CarFuelCardUpdateForm

    def form_valid(self, form):
        self.object = form.save()
        # В Карточках убираем привязанную машину, в машинах - привязанную карточку обновляем
        try:
            old_card_object = FuelCards.objects.get(assigned_to_car=self.object.pk)
            old_card_object.assigned_to_car = None
            old_card_object.save()
        except ObjectDoesNotExist:
            pass
        card_object = FuelCards.objects.get(pk=self.object.fuel_card.pk)
        card_object.assigned_to_car = self.object
        card_object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if self.request.GET.get('return_url'):
            return self.request.GET.get('return_url')
        else:
            return reverse('car_card', args=(self.object.id,))


class CarDocsView(LoginRequiredMixin, UpdateView):
    template_name = "car/car_docs.html"
    model = CarDocs
    form_class = CarDocsForm

    def get_object(self, queryset=None):
        car_pk = self.kwargs.get('car_pk', None)
        try:
            object = CarDocs.objects.get(car=car_pk)
            return object
        except CarDocs.DoesNotExist:
            return None

    def get_initial(self):
        initial = {'car': self.kwargs.get('car_pk', None)}
        return initial

    def get_success_url(self):
        car_pk = self.kwargs.get('car_pk', None)
        return reverse('car_card', args=(car_pk,))

    def get_context_data(self, *args, **kwargs):
        context_data = super(CarDocsView, self).get_context_data(**kwargs)
        car_pk = self.kwargs.get('car_pk', None)
        context_data['car'] = Cars.objects.get(pk=car_pk)
        return context_data


class SpeedometerChangeAddView(LoginRequiredMixin, CreateView):
    template_name = 'car/car_speedometer_change.html'
    form_class = SpeedometerChangeForm
    model = Cars

    def get_initial(self):
        initial = {'car': self.kwargs.get('pk', None)}
        return initial

    def get_context_data(self, *args, **kwargs):
        context_data = super(SpeedometerChangeAddView, self).get_context_data(*args, **kwargs)
        car_pk = self.kwargs.get('pk', None)
        context_data['car'] = Cars.objects.get(pk=car_pk)
        return context_data

    def get_success_url(self):
        car_pk = self.kwargs.get('pk', None)
        return reverse('car_speedometer_change', args=(car_pk,))

    def get_speedometer_change_log(self):
        return SpeedometerChangeLog.objects.filter(car=self.kwargs.get('pk', None))

