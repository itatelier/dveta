# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix, JsonUpdateObject
from django.http import HttpResponse

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.apps import apps
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404


class DumpPriceAddView(LoginRequiredMixin, CreateView):
    template_name = 'dump/dummp_price_add.html'
    form_class = DumpPriceAdd
    success_url = '/'
    queryset = DumpPrices.objects.all()

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(DumpPriceAddView, self).get_context_data(*args, **kwargs)
    #     person_pk = self.kwargs.get('pk', None)
    #     context_data.update({
    #     })
    #     return context_data

    # def post(self, request, *args, **kwargs):
    #     person_pk = self.kwargs.get('pk', None)
    #     form = self.get_form()
    #     if form.is_valid():
    #         person_object = Persons.objects.get(pk=person_pk)
    #         contact_object = form.save(commit=False)
    #         contact_object.person = person_object
    #         contact_object.save()
    #         self.success_url = '/persons/%s/contacts' % person_pk
    #         return HttpResponseRedirect(self.success_url)
    #     else:
    #         self.object = form.instance
    #         for field in form:
    #             for err in field.errors:
    #                 log.warn("Field %s Err: %s" % (field.name, err))
    #         return self.render_to_response(self.get_context_data(form=form))