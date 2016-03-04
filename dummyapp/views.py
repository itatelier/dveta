from django.shortcuts import render
from django.views.generic.base import TemplateView
from common.mixins import LoginRequiredMixin, PermissionRequiredMixin, DeleteNoticeView
#REST
from django.contrib.auth.models import User, Group
from dummyapp.models import *
from rest_framework import viewsets, generics, filters
import django_filters
from dummyapp.serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, _get_count, LimitOffsetPagination, _positive_int
from rest_framework.settings import api_settings


import logging
log = logging.getLogger('django')


class DummyListingIndex(LoginRequiredMixin, TemplateView):
    template_name = "dummy/listing.html"


class CompanyFilters(django_filters.FilterSet):
    name_ac = django_filters.CharFilter(name="name", lookup_type='icontains')
    date_after = django_filters.DateFilter(input_formats=('%d-%m-%Y',), name="date_add", lookup_type='gte')

    class Meta:
        model = DummyCompanies
        fields = ['name', 'date_after', 'name_ac', 'status', 'org_type']


class CompanyViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    queryset = DummyCompanies.objects.select_related('org_type', 'rel_type', 'status')
    serializer_class = CompanySerializer
    filter_class = CompanyFilters
    search_fields = ('www', 'description')
    ordering_fields = ('name', 'status', 'org_type', 'rel_type', 'date_add')


class RawPaginator(LimitOffsetPagination):
    default_limit = api_settings.PAGE_SIZE
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None
    template = 'rest_framework/pagination/numbers.html'

    def _get_count(queryset):
        """
        Determine an object count, supporting either querysets or regular lists.
        """
        try:
            return queryset.count()
        except (AttributeError, TypeError):
            return len(queryset)

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.offset = self.get_offset(request)
        self.count = _get_count(queryset)
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True
        return list(queryset[self.offset:self.offset + self.limit])

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                return _positive_int(
                    request.query_params[self.limit_query_param],
                    cutoff=self.max_limit
                )
            except (KeyError, ValueError):
                pass

        return self.default_limit

    def get_offset(self, request):
        try:
            return _positive_int(
                request.query_params[self.offset_query_param],
            )
        except (KeyError, ValueError):
            return 0


class DummyFlowViewSet(viewsets.ModelViewSet):
    serializer_class = DummyFlowSerializer
    pagination_class = RawPaginator
    queryset = DummyFlow.objects.get_flow()

    def get_queryset(self):
        qs = DummyFlow.objects.raw("""SELECT
                                            i.transaction_id
                                            ,o.transaction_id as id
                                            ,ABS(o.qty) as qty_o
                                            ,i.qty as qty_i
                                            ,o.id as id_o
                                            ,i.id as id_i
                                          ,o.object_id as object_id_o
                                          ,i.object_id as object_id_i
                                    FROM
                                            dummy_flow AS o
                                    LEFT JOIN dummy_flow AS i ON i.transaction_id = o.transaction_id AND i.object_id != o.object_id
                                    WHERE
                                            (i.id IS NOT NULL AND i.qty > 0) OR i.id IS NULL
                                    ORDER BY id
                                    """)
        return qs

    # def paginate_queryset(self, queryset):
    #     return self.paginator.paginate_queryset(list(queryset), self.request, view=self)