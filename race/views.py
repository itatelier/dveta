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

    def get(self, *args, **kwargs):
        # form = self.form_class
        self.object = None
        # Полям формы присваивается пустой QS, что бы не тянуть всю талицу в Choices для селекта
        form = none_modelchoicesfields_querysets(self.form_class, ('company', 'contragent', 'place'))
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, *args, **kwargs):
        context_data = super(RaceCreateView, self).get_context_data(*args, **kwargs)
        form = self.form_class
        # context_data.update({'formdict': "hz"})
        return context_data

    def get_success_url(self):
        return reverse('car_card', args=(self.object.id,))

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        car_pk = self.kwargs.get('car_id', None)

        # Полям формы снова присваивается полный QS, для парвильной валидации поля.
        form.fields["company"].queryset = Companies.objects.all()
        form.fields["contragent"].queryset = Contragents.objects.all()
        form.fields["place"].queryset = Objects.objects.all()

        if form.is_valid():
            # смежные объекты
            car_obj = Cars.objects.get(pk=car_pk)
            object_obj = Objects.objects.get(pk=self.request.POST.get('place', None))
            # Объект формы (Race object)
            race_object = form.save(commit=False)
            race_object.car = car_obj
            race_object.driver = car_obj.driver
            race_object.object = object_obj
            race_object.save()
            self.success_url = '/races/%s/update' % race_object.id
            return HttpResponseRedirect(self.success_url)
        else:
            # Удаляем queryset из перечисленных полей, что бы генератор не поставил для Select'a всю таблицу из БД.
            # вместо QuerySet добавляем Choices с единичной записью
            form = replace_modelchoicesfields_data(form, ('company', 'contragent', 'place'))
            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))


class RaceUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'race/race_update.html'
    form_class = RaceUpdateForm
    model = Races

    def get_success_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        return "/races/%s/update" % pk

    def get_context_data(self, *args, **kwargs):
        context_data = super(RaceUpdateView, self).get_context_data(*args, **kwargs)
        race_pk = self.kwargs.get('pk', None)
        context_data['race'] = Races.objects.get(pk=race_pk)
        return context_data