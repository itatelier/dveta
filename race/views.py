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
from dds.models import *
from dump.models import TalonsFlow
from common.models import Variables
from salary.models import SalaryTarifPlans


class RaceCreateView(LoginRequiredMixin, CreateView):
    template_name = 'race/race_create.html'
    form_class = RaceCreateForm
    model = Races

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
        if form.is_valid():
            # смежные объекты 
            car_obj = Cars.objects.get(pk=car_pk)
            object_obj = Objects.objects.get(pk=self.request.POST.get('place', None))
            # Объект формы (Race object)
            race_object = form.save(commit=False)
            race_object.car = car_obj
            race_object.driver = car_obj.driver
            race_object.object = object_obj
            # В шаблоне есть hidden input: is_mark_required. Его значение устанавливается после функции инфо о клиенте
            if form.cleaned_data['is_mark_required']:
                race_object.mark_required = True
            log.info(u"---- Dump: %s  PAy type: %s Dump object param: %s  Object pay type: %s" % (form.cleaned_data['dump'], form.cleaned_data['dump_pay_type'], race_object.dump, race_object.dump_pay_type))

            # Создаем запись в журнале талонов
            if race_object.dump and race_object.dump_pay_type == True:
                log.info("---- Расход талона! Dump group: %s" % race_object.dump.group.pk)
                proc_result, proc_error = TalonsFlow.objects.move_between_proc(
                    1,                          # Тип операции РАСХОД
                    race_object.dump.group.pk,  # Группа полигона
                    1,                          # Количество расходуемых талонов
                    race_object.driver.pk,      # Сотрудник, с которого снимают талон (водитель)
                    0,                          # Пусто, нет сотрудника для передачи талона
                    1,                          # Группа талонодержателей ВОДИТЕЛИ
                    0                           # Пусто, Группа талонодержателей получателя не используется
                )
                if proc_result != 1:
                    form.add_error(None, proc_error)
                    self.object = form.instance
                    return self.render_to_response(self.get_context_data(form=form))
            # Обновление ДДС
            if race_object.pay_way:  # если оплата Безналичная
                DdsFlow.objects.flow_move(
                    item_out_id=18,
                    account_out_id=race_object.contragent.money_account.get().pk,
                    pay_way_out=True,
                    item_in_id=4,
                    account_in_id=5,
                    pay_way_in=True,
                    summ=race_object.sum
                 )
            else:       # если оплата Нал
                DdsFlow.objects.flow_op(
                    17,
                    # race_object.contragent.money_account.get().pk,
                    race_object.driver.money_account.get().pk,
                    False,  # тип оплаты - нал
                    race_object.sum,
                    True  # Тип операции - приход
                )
            # Расчет вознаграждения водителя
            # Если в объекте указана спец.цена - она без доп. расчетов помещается в рейс, если нет, то расчет идет по
            # тарифам в зависимости от типа загрузки: рогатка, Мультилифт и т.п.
            if object_obj.salary_spec_price > 0:
                race_object.salary_driver_sum = object_obj.salary_spec_price
                race_object.salary_tarif_id = 1
            else:
                car_load_type = car_obj.load_type
                salary_tarif_object = SalaryTarifPlans.objects.get(car_load_type=car_load_type)
                race_object.salary_driver_sum = salary_tarif_object.standart_tarif
                race_object.salary_tarif_id = salary_tarif_object.id
            salary_driver_sum = 0
            # if object_obj.salary_spec_price > 0:
            #     salary_driver_sum = race_object.hodkis * object_obj.salary_spec_price
            # else:
            #     variable_tarif_standart_hodki = Variables.objects.get(pk=1)
            #     salary_driver_sum = race_object.hodkis * variable_tarif_standart_hodki.val
            # race_object.salary_driver_sum = salary_driver_sum

            race_object.save()
            self.success_url = '/races/%s/update' % race_object.id
            return HttpResponseRedirect(self.success_url)
        else:
            form = replace_form_choices_select2(form, ('company', 'contragent', 'place'))
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


class RacesViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = Races.objects.select_related(
        'race_type',
        'cargo_type',
        'company',
        'contragent',
        'object',
        'car',
        'driver',
        'dump',
        'bunker_type',
        # 'employies'
    ).prefetch_related(
        'driver__status',
        'driver__person'
    )
    serializer_class = RaceSerializer
    search_fields = ('object__name', 'object__street')
    filter_class = RaceFilters
    ordering_fields = ('car', 'driver__nick', 'company__name', 'contragent__name')


class RacesListView(LoginRequiredMixin, TemplateView):
    template_name = 'race/list_races.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super(RacesListView, self).get_context_data(*args, **kwargs)
        context_data['bunker_types'] = BunkerTypes.objects.all()
        context_data['get'] = self.request.GET
        # context_data['company'] = Companies.objects.get(pk=company_pk)
        # context_data['bunker_types_summ'] = ('type1_summ', 'type2_summ', 'type3_summ', 'type4_summ', 'type5_summ', 'type6_summ', 'type7_summ', )
        return context_data

