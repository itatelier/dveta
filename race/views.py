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
from serializers import *


class RaceCreateView(LoginRequiredMixin, CreateView):
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