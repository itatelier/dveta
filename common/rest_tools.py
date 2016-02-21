# -*- coding:utf-8 -*-

from django.db.models import Model
from django.db import connection
import datetime
from collections import namedtuple


import logging
log = logging.getLogger('django')


def action_at_evening(queryset, value):
    log.info("Action val: %s" % value)
    value = "%s 23:59:59" % value
    return queryset.filter(
        date__lte=value,
    )


