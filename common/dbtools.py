# -*- coding:utf-8 -*-

from django.db.models import Model
from django.db import connection
import datetime
from collections import namedtuple


import logging
log = logging.getLogger('django')


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def fetch_sql_allintuple(query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    return namedtuplefetchall(cursor)


def fetch_sql_row(query, params):
    cursor = connection.cursor()
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row

