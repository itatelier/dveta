# -*- coding: utf8 -*

from django import template
from datetime import datetime, timedelta
from django.utils.timesince import timesince
from common.utils import dney_str

import logging
log = logging.getLogger('django')

register = template.Library()


@register.filter
def timesince_threshold(value, days=7):
    """
    return timesince(<value>) if value is more than <days> old. Return value otherwise
    """
    log.info("--- Value: %s" % value)
    if datetime.now() - value < timedelta(days=days):
        return timesince(value)
    else:
        return value

timesince_threshold.is_safe = False


@register.filter
def check_days_to_now(value_date, days):
    now = datetime.now()
    delta_date = now + timedelta(days=days)
    remain_days = now - value_date
    # log.info("--- Now: %s  Value_date: %s  Delta: %s Remain days: %s" % (now.date(), value_date, delta_date.date(), \
    # remain_days.days))
    if value_date < delta_date:
        if int(remain_days.days) < 0:
            return "осталось %s %s" % (abs(remain_days.days), dney_str(abs(remain_days.days)))
        else:
            return "просрочено на %s %s" % (abs(remain_days.days), dney_str(abs(remain_days.days)))
    else:
        return False

check_days_to_now.is_safe = False
