# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from bunker.models import BunkerFlow
from object.models import ObjectTypes
from forms import *


# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView
from django.db.models import Sum

# API
from serializers import *
from person.serializers import *
from rest_framework import viewsets, generics, filters


class CarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'car/car_create_update.html'
    form_class = CarCreateForm
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
            create_object = form.save(commit=False)
            create_object.car_object = car_object
            create_object.save()
            self.success_url = '/cars/%s/card' % create_object.id
            return HttpResponseRedirect(self.success_url)
        else:
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class CarCardView(LoginRequiredMixin, DetailView):
    template_name = "car/car_card.html"
    model = Cars
    queryset = Cars.objects.select_related('model', 'model__brand', 'fuel_type', 'unit_group', 'car_object', 'mechanic', 'mechanic__person')

    def get_context_data(self, *args, **kwargs):
        context_data = super(CarCardView, self).get_context_data(*args, **kwargs)
        context_data['bunkers_onboard'] = BunkerFlow.objects.filter(object__pk=self.object.car_object.id).aggregate(Sum('qty'))
        return context_data


class CarUpdateView(LoginRequiredMixin, UpdateView):
        template_name = "car/car_create_update.html"
        model = Cars
        form_class = CarCreateForm

        def get_success_url(self):
            return reverse('car_update', args=(self.object.id,))


class CarsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Cars.objects.filter().select_related('model', 'model__brand', 'fuel_type', 'unit_group', 'car_object', 'mechanic', 'mechanic__person', 'mechanic__type', 'mechanic__role', 'mechanic__status')
    serializer_class = CarsSerizlizer
    filter_class = CarFilters
    search_fields = ('pk', 'model', 'reg_num', 'nick_name', )
    ordering_fields = ('model', 'fuel_type', 'mechanic', 'unit_group', 'reg_num', 'nick_name', 'trailer_attached', 'date_add')