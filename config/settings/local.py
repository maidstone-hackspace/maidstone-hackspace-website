# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use mailhog for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket
import os
from .common import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='wq)sg12k&5&adv)e%56n5e97o@))6xu90b**=-w+)d^c+cd9%1')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_PORT = 1025

EMAIL_HOST = env("EMAIL_HOST", default='mailhog')
MSG_PREFIX = 'MHT'


# CACHING
# ------------------------------------------------------------------------------

REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL', default='redis://redis:6379'), 0)
# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
                                        # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        }
    },
    'st_rate_limit': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'spirit_rl_cache',
        'TIMEOUT': None
    }
}


# django-debug-toolbar
# ---------------------MDVTDNXFTRJSJBX9KWOJTMCGSNMYASEFNBPDUZJMGSPPCVMQRUZMZAEXDTIGHPZCP9JBGLVKGSJMZKPVV---------------------------------------------------------
MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', ]
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions', )
INSTALLED_APPS += ('storages', )

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
# CELERY_ALWAYS_EAGER = True
########## END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
CAPTCHA = {
    'secret': '',
    'site': ''
}

WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename': "%s/django.log" % ROOT_DIR,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'logfile'],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['logfile', 'console', 'mail_admins'],
            'propagate': True
        }
    }
}

PAYMENT_PROVIDERS['gocardless']['redirect_url'] = 'http://127.0.0.1:8180'
TEMPLATE_DEBUG = False


AWS_S3_SECURE_URLS = False
AWS_ACCESS_KEY_ID = env('MINIO_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = env('MINIO_SECRET_KEY')


AWS_S3_ENDPOINT_URL = 'http://%s:9000' % socket.gethostbyname('bucket')


# AWS_S3_SECURE_URLS = True
# AWS_ACCESS_KEY_ID = env('DIGITALOCEAN_SPACE_KEY')
# AWS_SECRET_ACCESS_KEY = env('DIGITALOCEAN_SPACE_SECRET')
# AWS_S3_ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'
AWS_STORAGE_BUCKET_NAME = 'mhackspace'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'dev'
AWS_S3_SECURE_URLS = True
STATIC_URL = '%s/%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

COMPRESS_URL = '%s/%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME, AWS_LOCATION)
