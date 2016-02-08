# -*- coding: utf8 -*

# App spcific
from models import *
from company.models import *
from forms import *

# Base Views
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView, JsonViewMix
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView


class CarCreateView(LoginRequiredMixin, CreateView):
    template_name = 'car/car_create.html'
    form_class = CarCreateForm
    model = Cars

    def get_success_url(self):
        return reverse('car_card', args=(self.object.id,))


class CarCardView(LoginRequiredMixin, DetailView):
    template_name = "car/car_card.html"
    model = Cars

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(CarCardView, self).get_context_data(*args, **kwargs)
    #     # object = Companies.objects.select_related('rel_type', 'org_type', 'status', 'client_options', 'attr_source').prefetch_related('contact').get(pk=kwargs['pk'])
    #     context_data.update({
    #         # 'object': object,
    #         # 'contacts': CompanyContacts.objects.select_related('company', 'contact').filter(company__pk=object.pk, show_in_card=True),
    #     })
    #     return context_data