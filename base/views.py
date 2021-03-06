# -*- coding: utf8 -*

from django.views.generic import TemplateView, View
from common.mixins import JsonViewMix
from django.http import HttpResponse
from django.db.models import Count
from django.apps import apps
import json
import pickle
from django.http import HttpResponse, HttpResponseForbidden


import logging
# from company.models import *

log = logging.getLogger('django')


class Forbidden(TemplateView):
    template_name = "forbidden.html"


class Index(TemplateView):
    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        context_data = super(Index, self).get_context_data(*args, **kwargs)
        context_data.update({
            'some_strange_variable': 42,
        })
        return context_data


class PlaygroundCard(TemplateView):
    template_name = "pg/card.html"


class PlaygroundListing(TemplateView):
    template_name = "pg/listing.html"


class PlaygroundForms(TemplateView):
    template_name = "pg/forms.html"


class AutoCompliteJsonView(JsonViewMix):
    param_names = ['model', 'field', 'query', 'filter_type', 'model_manager']

    # тут параметр 'model_manager' нужен для того, что бы иметь возможность задать Queryset точнее
    # Менеджер по умолчанию для любой модели это 'objects'

    def prepare(self, request, *args, **kwargs):
        model_param_value = self.values['model']
        try:
            model = apps.get_model(*model_param_value.split('.'))
        except LookupError:
            self.errors.append("Model \'%s\' not found!" % model_param_value)
            return
        field = self.values['field']
        default_model_manager = 'objects'
        queryset_manager = default_model_manager
        param_model_manager = self.values['model_manager']
        if param_model_manager:
            queryset_manager = param_model_manager
        qs = getattr(model, queryset_manager)
        qs = qs.values_list(field)
        if self.values['query']:
            sort_criteria = self.values['field'] + self.values['filter_type']
            sort_value = self.values['query']
            filters = {sort_criteria: sort_value}
            qs = qs.filter(**filters).annotate(aggregate=Count(field))[:10]
        self.data = list(qs)


class GetContactByPhoneJsonView(JsonViewMix):
    param_names = ['number']
    model_name = 'person.Contacts'

    def prepare(self, *args, **kwargs):
        try:
            model = apps.get_model(self.model_name)
        except LookupError:
            self.errors.append("Model \'%s\' not found!" % self.model_name)
            return
        log.info("Model param value: %s model object: %s" % (self.model_name, model))
        field = self.values['number']
        filters = {'phonenumber': field}
        qs = model.objects.filters(**filters).select_related('person').values_list()
        self.data = list(qs)


