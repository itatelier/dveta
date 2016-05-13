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
from serializers import *
from contragent.models import *
from rest_framework import viewsets, generics, filters
from django.http import HttpResponseRedirect


class AccountsViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = DdsAccounts.objects.select_related(
        'type',
        'contragent',
        'employee',
    ).prefetch_related(
        'employee__person'
    )
    serializer_class = AccountsSerializer
    search_fields = ('name', 'contragent_name', 'employee__person__family_name')
    filter_class = AccountsFilters
    ordering_fields = ('pk', 'contragent__name', 'balance')


class AccountRefillView(LoginRequiredMixin, CreateView):
    template_name = 'dds/account_refill.html'
    form_class = AccountRefillForm
    model = DdsFlow


    # def get(self, *args, **kwargs):
    #     # form = self.form_class
    #     self.object = None
    #     # Полям формы присваивается пустой QS, что бы не тянуть всю талицу в Choices для селекта
    #     form = none_modelchoicesfields_querysets(self.form_class, ('company', ))
    #     return self.render_to_response(self.get_context_data(form=form))

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super(AccountRefillView, self).get_context_data(*args, **kwargs)
    #     companny_id = self.request.POST.get('company', None)
    #     form = self.form_class
    #     # context_data.update({'formdict': "hz"})
    #     form.fields['company'].queryset = Companies.objects.filter(pk=companny_id)
    #     context_data.update({'form': form})
    #     return context_data

    def get_success_url(self):
        # return reverse('car_card', args=(self.object.id,))
        return reverse('races_list', args=())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = '/races/list/'
            return HttpResponseRedirect(self.success_url)
        else:
<<<<<<< HEAD
=======
            # Удаляем queryset из перечисленных полей, что бы генератор не поставил для Select'a всю таблицу из БД.
            # вместо QuerySet добавляем Choices с единичной записью
            # for key in form.cleaned_data:
            #     print "--- Clean data key: %s" % key
            # company_id = form.cleaned_data["company"]
            # log.info("--- company_id: %s" % company_id )
            # form.fields["company"].queryset = Companies.objects.filter(pk=company_id)
            form = replace_modelchoicesfields_data(form, ('company',))
>>>>>>> origin/master
            self.object = form.instance
            form = replace_form_choices_select2(form, ('company',))
            return self.render_to_response(self.get_context_data(form=form))
