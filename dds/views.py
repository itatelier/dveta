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
        # car_pk = self.kwargs.get('car_id', None)

        # Полям формы снова присваивается полный QS, для парвильной валидации поля.
        # form.fields["company"].queryset = Companies.objects.all()
        # form.fields["contragent"].queryset = Contragents.objects.all()
        # form.fields["place"].queryset = Objects.objects.all()

        if form.is_valid():
            new_object = form.save(commit=False)
            new_object.save()
            self.success_url = '/races/list/'
            return HttpResponseRedirect(self.success_url)
        else:
            # Удаляем queryset из перечисленных полей, что бы генератор не поставил для Select'a всю таблицу из БД.
            # вместо QuerySet добавляем Choices с единичной записью
            # for key in form.cleaned_data:
            #     print "--- Clean data key: %s" % key
            # company_id = form.cleaned_data["company"]
            # log.info("--- company_id: %s" % company_id )
            # form.fields["company"].queryset = Companies.objects.filter(pk=company_id)
            form = replace_modelchoicesfields_data(form, ('company',))

            self.object = form.instance
            return self.render_to_response(self.get_context_data(form=form))
