# -*- coding: utf8 -*

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.http import urlquote
from common.utils import JsonResponseContext, GetInstanceValues
from django.views.generic import View
from django.views.generic.edit import DeleteView
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
#import simplejson as json
import json
import logging
from datetime import date, timedelta
from django.core.paginator import Paginator
# from company.models import Companies
from django.shortcuts import render_to_response
from django.contrib.auth.views import redirect_to_login
from django import http
# from django.db.models import get_model
from django.apps import apps
import datetime
import decimal
from django.utils.timezone import is_aware


log = logging.getLogger('django')


class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class PermissionRequiredMixin(object):
    """
    View mixin which verifies that the logged in user has the specified
    permission.

    Class Settings
    `permission_required` - the permission to check for.
    `login_url` - the login url of site
    `redirect_field_name` - defaults to "next"
    `raise_exception` - defaults to False - raise 403 if set to True

    Example Usage

        class SomeView(PermissionRequiredMixin, ListView):
            ...
            # required
            permission_required = "app.permission"

            # optional
            login_url = "/signup/"
            redirect_field_name = "hollaback"
            raise_exception = True
            ...
    """
    login_url = settings.LOGIN_URL
    permission_required = None
    raise_exception = False
    redirect_field_name = 'next'

    def dispatch(self, request, *args, **kwargs):
        # Verify class settings
        if self.permission_required == None or len(
                self.permission_required.split(".")) != 2:
            raise ImproperlyConfigured("'PermissionRequiredMixin' requires "
                                       "'permission_required' attribute to be set.")

        has_permission = request.user.has_perm(self.permission_required)

        if not has_permission:
            if self.raise_exception:
                return HttpResponseForbidden()
            else:
                path = urlquote(request.get_full_path())
                tup = self.login_url, self.redirect_field_name, path
                # return HttpResponseRedirect("%s?%s=%s" % tup)
                return HttpResponseRedirect("/forbidden")

        return super(PermissionRequiredMixin, self).dispatch(
            request, *args, **kwargs)


class DeleteNoticeView(DeleteView):
    template_name = "confirm_delete_object.html"
    notice = False

    def get_context_data(self, *args, **kwargs):
        context_data = super(DeleteNoticeView, self).get_context_data(*args, **kwargs)
        context_data.update({
            'notice': self.notice,
        })
        return context_data


class _JsonObjectViews(View):
    model_name = None
    required_params = ['pk', 'colname', 'value']
    inicial_data = {}

    def __init__(self, *args, **kwargs):
        self.json = {}
        self.errors = []
        self.update_data = {}
        super(_JsonObjectViews, self).__init__(*args, **kwargs)

    def check_required_params(self, required_params):
        if not self.model_name:
            self.errors.append("No model specified!")
            return False
        for param in required_params:
            if param not in self.inicial_data:
                if param not in self.request.GET or self.request.GET[param] == '':
                    self.errors.append("Parameter '%s' required, not found" % param)
                    return False
                else:
                    self.update_data[param] = self.request.GET[param]
            else:
                self.update_data[param] = self.inicial_data[param]
        return True

    def to_json(self, ret):
        self.json['GET'] = self.request.GET
        if len(self.errors) > 0:
            self.json['result'] = 0
            self.json['errors'] = self.errors
        else:
            self.json['result'] = 1
            self.json['update_data'] = self.update_data
        json_ret = json.dumps(ret, indent=2)
        return  json_ret

    def _get_model(self, model_name):
        model = apps.get_model(*model_name.split('.'))
        return model

    def _get_object(self, model):
        try:
            obj = model.objects.get(pk=self.update_data['pk'])
            return obj
        except model.DoesNotExist:
            self.errors.append("Object not found! pk=%s" % self.update_data['pk'] )
        return


class JsonUpdateObject(_JsonObjectViews):
    def update_object(self, data):
        model = self._get_model(self.model_name)
        obj = self._get_object(model)
        if obj:
            log.info("Updating object with colname [%s] and value: %s" % (data['colname'], data['value']))
            setattr(obj, data['colname'], data['value'])
            obj.save()

    def get(self, request, *args, **kwargs):
        if self.check_required_params(self.required_params):
            self.update_object(self.update_data)
        return HttpResponse(self.to_json(self.json), mimetype='text/plain')


class JsonDeleteObject(_JsonObjectViews):
    required_params = ['pk',]

    def update_object(self, data):
        model = self._get_model(self.model_name)
        obj = self._get_object(model)
        if obj:
            obj.delete()

    def get(self, request, *args, **kwargs):
        if self.check_required_params(self.required_params):
            self.update_object(self.update_data)
        return HttpResponse(self.to_json(self.json), mimetype='text/plain')


class JsonListMixin(View):
    log.info("CLASS PRELOAD")
    params = {}
    qs = False
    data = False
    qs_filters = {}
    relations = {}

    def __init__(self, *args, **kwargs):
        log.info("CLASS INIT")
        self.values = {}
        self.errors = []
        self.result = False
        self.json = {}
        self.json_data = None
        self.get_params = {}
        super(JsonListMixin, self).__init__(*args, **kwargs)

    def check(self, request):
        ## Request params
        request_values = {}
        ## Cheking setting defaults for empty or null params
        for key, val in self.params.iteritems():
            if key in self.request.GET and self.request.GET[key] != '' and self.request.GET[key] != 'reset':
                request_values[key] = self.request.GET[key]
                #log.info("Param [%s] is in get, value: %s" % (key, request_values[key]))
            else:
                if self.params[key]['default']:
                    request_values[key] = self.params[key]['default']
                else:
                    self.errors.append("Request parameter \'%s\' not found in request or no default specified!" % key)
        ## Assigning request values to Class dict values
        self.values = request_values
        if len(self.errors) > 0:
            return False
        else:
            return True

    def to_json(self):
        if len(self.errors) > 0:
            self.json['result'] = 0
            self.json['errors'] = self.errors
        else:
            self.json['result'] = 1
            self.json['values'] = self.values
        json_params = json.dumps(self.json, indent=2)
        ret = "{\n \"data\": " + self.json_data + ",\n \"response\": " + json_params + "\n}"
        return ret

    def get(self, request, *args, **kwargs):
        if not self.qs:
            self.errors.append("QuerySet not specified!")
        if self.check(request):
            log.info("CHECK PASSED")
           ## Building QuerySet filters
            filters = {}
            for key, val in self.params.iteritems():
                if 'type' in val and self.values[key] != 'reset':
                    if val['type'] == 'filter':
                        filters[key] = self.values[key]
                    elif val['type'] == 'text':
                        param = val['field'] + val['filter_type']
                        filters[param] = self.values[key]
                    elif val['type'] == 'in':
                        filters[param] = request.GET.getlist(key)
                    elif val['type'] == 'bool':
                        if self.values[key] == "False":
                            filters[key] = False
                        elif self.values[key] == "True":
                            filters[key] = True
            if len(filters.keys()) > 0:
                self.qs = self.qs.filter(**filters)
                self.values['QuerySet Filters'] = filters

            ## Sorting
            sort_order = []
            if self.values['sort_way'] == "+":
                self.values['sort_way'] = ''
            if self.values['sort_col'] == 'reset':
                sort_order.append(self.params['sort_col']['default'])
            else:
                sort_order.append(self.values['sort_way'] + self.values['sort_col'])
            self.values['sort_order'] = sort_order

            ## Applying Sort order to QuerySet
            if len(sort_order) > 0:
                self.qs = self.qs.order_by(*sort_order)

            ## Runing QuerySet for current page
            page_num = int(self.values['page'])
            p = Paginator(self.qs, self.values['rows'])
            page = p.page(page_num)
            self.values['total_pages'] = p.num_pages
            self.json_data = self.data_to_json(page)

            ## Pager
            self.values['pager'] = {'next_num': page_num + 1, 'prev_num': page_num - 1, 'current_num': page_num, 'total_num': p.num_pages }
        return HttpResponse(self.to_json(), mimetype='text/plain')


    def data_to_json(self, data):
        return serializers.serialize('json', data, indent=2, relations=self.relations)

    def data_to_json_old(self, data):
        values = {}
        for el in data:
            #el_values = GetInstanceValues(el, go_into={'company': {'extra':{'mphone':{}}}, 'address': {}, 'mphone': {}},)
            el_values = GetInstanceValues(el)
            values.setdefault(el.id, el_values)
        jsondata = json.dumps(values, encoding='utf8', cls=DjangoJSONEncoder)
        return jsondata


class JsonViewMix(View):
    param_names = []
    qs = False
    data = False
    login_required = True

    def __init__(self, *args, **kwargs):
        self.values = {}
        self.errors = []
        self.result = True
        self.json = {}
        self.get_params = {}
        super(JsonViewMix, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated():
            self.errors.append("Auth required, but not!")
        return HttpResponse(self.to_json(), content_type='text/plain')

    def get(self, request, *args, **kwargs):
        if self.login_required and not request.user.is_authenticated():
            return redirect_to_login(request.path)
        if self.check(request):
            self.prepare(request)
        return HttpResponse(self.to_json(), content_type='text/plain')

    def prepare(self, request, *args, **kwargs):
        '''
        Метод для подготовки в наследуемых классах
        '''
        return

    def check(self, request):
        self.get_params = request.GET
        for name in self.param_names:
            if name in self.get_params and self.get_params[name] != '':
                self.values[name] = self.get_params[name]
            else:
                self.errors.append("Request parameter \'%s\' not found!" % name)
        if len(self.errors) > 0:
            self.result = False
        return self.result

    def to_json(self):
        if self.qs:
            self.json['data'] = json.loads(serializers.serialize('json', self.qs, indent=2))
        elif self.data:
            self.json['data'] = self.data
        if len(self.errors) > 0:
            self.json['result'] = 0
            self.json['errors'] = self.errors
        else:
            self.json['result'] = 1
            self.json['values'] = self.values
        ret = json.dumps(self.json, indent=2)
        return ret

