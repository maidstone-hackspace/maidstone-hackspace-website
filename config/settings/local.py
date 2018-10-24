# -*- coding: utf-8 -*-

import socket
import os
from .common import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=True)
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# ALLOWED_HOSTS = ['*']
# INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', '172.22.0.9', '192.168.1.113', '172.22.0.4', '0.0.0.0']
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    # ip = socket.gethostbyname('nginx')
    INTERNAL_IPS += [ip[:-1] + "1"]
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1"]

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
INSTALLED_APPS += ('debug_toolbar', )
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}


# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_TASK_ALWAYS_EAGER = True
########## END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
CAPTCHA = {
    'secret': '',
    'site': ''
}


# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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
            'filename': "/tmp/django.log"
        },
    },
    'loggers': {
        'mhackspace': {
          'level': 'DEBUG',
            'handlers': ['console']
        },
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


# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------


PAYMENT_PROVIDERS['gocardless']['redirect_url'] = 'http://127.0.0.1:8180'
TEMPLATE_DEBUG = True 

AWS_S3_SECURE_URLS = False
AWS_ACCESS_KEY_ID = env('BUCKET_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = env('BUCKET_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = 'mhackspace-local'
AWS_S3_ENDPOINT_URL = 'http://%s:9000' % socket.gethostbyname('bucket')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'dev'
AWS_S3_SECURE_URLS = True
STATIC_URL = '%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME)



# COMPRESSOR
# ------------------------------------------------------------------------------
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)
COMPRESS_STORAGE = STATICFILES_STORAGE
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
