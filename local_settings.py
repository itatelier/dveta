import os
import sys

sys.path.append('C:/Python27/Lib/site-packages/django_debug_toolbar-1.4.dist-info/')

ROOT_PATH = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'veta',                      # Or path to database file if using sqlite3.
        'USER': 'root',
        'PASSWORD': 'vfcnth1Key',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# TEMPLATE_DIRS = (
#     ROOT_PATH + "/templates/",
# )


# ========= DEBUG =========

INTERNAL_IPS = ('127.0.0.1')