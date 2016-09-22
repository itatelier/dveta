# -*- coding: utf8 -*

from models import SalaryMonthSummary
from race.models import Races
from django.db.models import Sum
import calendar

import logging
log = logging.getLogger('django')

class DriverStats:
    def __init__(self, date_start, date_end, driver_pk):
        self.date_start = date_start
        self.date_end = date_end
        self.driver_pk = driver_pk
        self.list = None
        self.sumary = None

    def get_list(self):
        self.list = SalaryMonthSummary.objects.driver_month_stats(date_start=self.date_start, date_end=self.date_end, driver_pk=self.driver_pk)
        return self.list

    def get_summary(self):
        report_len = self.list.__len__()
        if report_len > 0:
            stats_summary = {}
            report_keys = ['races_done', 'total_hodkis', 'total_refuels', 'total_amount', 'total_run', 'fuel_overuse']
            # Если рейсы были на двух и более машинах
            for key in report_keys:
                key_value = 0
                for row in self.list:
                    if row._asdict()[key] is not None:
                        key_value += row._asdict()[key]
                stats_summary[key] = key_value
            stats_summary['km_on_hodkis'] = stats_summary['total_run'] / stats_summary['total_hodkis']
            return stats_summary
        return None


class RacesGraph:

    def __init__(self):
        self.year = None
        self.month = None
        self.driver_pk = None
        self.data = None
        self.days_list = None  # массив чисел календарных дней в заданом месяце
        self.month_days = None

    def getdata(self, year, month, driver_pk):
        # График - ходки по дням месяца
        races_qs = Races.objects.filter(date_race__year=year,
                                        date_race__month=month) \
            .extra({'dater': "day(date_race)"}).values('dater') \
            .annotate(sum=Sum('hodkis'))
        monthrange = calendar.monthrange(year, month)
        self.month_days = monthrange
        self.days_list = [x for x in range(1, monthrange[1] + 1)]
        races_graph_data = []
        for i in self.days_list:
            day_num = i
            day_count = 0
            for el in races_qs:
                if el['dater'] == day_num and el['sum'] > 0:
                    day_count = el['sum']
            races_graph_data.append(day_count)
        self.data = races_graph_data
        return self



