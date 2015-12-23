"""
"""
SECRET_KEY = 'l-9&@u1xkcm6-(+4^@*&$_)*tz*!7fllj$1vh#abfeyl*83+qu'
DEBUG = True

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = os.path.dirname(__file__)

DATABASES = ''
ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-RU'
DATE_FORMAT = "%d-%m-%Y"
DATE_INPUT_FORMATS = ('%d-%m-%Y', '%Y-%m-%d')
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = False
USE_THOUSAND_SEPARATOR = True
NUMBER_GROUPING = 3
DECIMAL_SEPARATOR = ","

STATIC_ROOT = 'c:/www/vetastatic'
STATIC_URL = '/static/'
STATICFILES_DIRS = (ROOT_PATH + '/static',)

MEDIA_ROOT = ROOT_PATH + '/media'
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    'dummyapp',
    'company',
    'contragent',
    'person'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'urls_root'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT_PATH, 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DATE_INPUT_FORMATS': ('%d-%m-%Y', '%Y-%m-%d'),
    'DATE_FORMAT': "%d-%m-%Y",
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

WSGI_APPLICATION = 'wsgi.application'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

try:
    from local_settings import *
except ImportError:
    pass