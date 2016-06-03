# -*- coding: utf8 -*

from django import template
from datetime import datetime, timedelta
from django.utils.timesince import timesince
from common.utils import dney_str

import logging
log = logging.getLogger('django')

register = template.Library()


@register.filter
def check_none(value, days=7):
    log.info("--- Value for check: %s type: %s" % (value, type(value)))
    if value == "None" or value == None:
        return False
    else:
        return True


check_none.is_safe = False
