# -*- coding: utf8 -*

from django.views.generic import TemplateView, View
# from common.mixins import JsonViewMix, JsonUpdateObject
from django.http import HttpResponse
from django.db.models import Count
import json
from django.db.models import get_model
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

# class ac(JsonViewMix):
#     param_names = ['model', 'field', 'query', 'filter_type']
#
#     def prepare(self):
#         model_param_value = self.values['model']
#         model = get_model(*model_param_value.split('.'))
#         log.info("Model param value: %s model: %s" % (model_param_value, model))
#         field = self.values['field']
#         qs = model.objects.values_list(field)
#         if self.values['query']:
#             sort_criteria = self.values['field'] + self.values['filter_type']
#             sort_value = self.values['query']
#             filters = {sort_criteria: sort_value}
#             qs = qs.filter(**filters).annotate(aggregate=Count(field))
#             #self.values['query'] = str(qs.query.__str__())
#         self.data = list(qs)
#
#
# class ac_with_id(View):
#
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             q = request.GET.get('query', '')
#             rows = Companies.objects.filter(name__icontains=q)[:20]
#             results = []
#             for row in rows:
#                 json_data = {}
#                 json_data['id'] = row.id
#                 json_data['label'] = row.name
#                 json_data['value'] = row.name
#                 results.append(json_data)
#             data = json.dumps(results)
#         else:
#             data = 'fail'
#         return HttpResponse(data, mimetype='text/plain')
#

