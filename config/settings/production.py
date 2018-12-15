# -*- coding: utf-8 -*-
"""
Production Configurations



"""
from __future__ import absolute_import, unicode_literals

from django.utils import six
from .common import *  # noqa

# SECURITY CONFIGURATION
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/1.9/ref/middleware/#module-django.middleware.security
# and https://docs.djangoproject.com/ja/1.9/howto/deployment/checklist/#run-manage-py-check-deploy

# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    'DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    'DJANGO_SECURE_CONTENT_TYPE_NOSNIFF', default=True)
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
#SECURE_SSL_REDIRECT = env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
CSRF_COOKIE_SECURE = True
#disabledd so csrf works with ajax
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = 'SAMEORIGIN'
X_FRAME_OPTIONS = 'ALLOW-FROM https://riot.im'

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['maidstone-hackspace.org.uk', 'live.maidstone-hackspace.org.ukhackdev_postgres_data_dev', 'www.maidstone-hackspace.org.uk'])
ALLOWED_HOSTS.append('127.0.0.1')
ALLOWED_HOSTS.append('172.18.0.5')

# END SITE CONFIGURATION


# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL',
                         default='Maidstone Hackspace <no-reply@maidstone-hackspace.org.uk>')
EMAIL_SUBJECT_PREFIX = env('DJANGO_EMAIL_SUBJECT_PREFIX', default='[Maidstone Hackspace] ')
SERVER_EMAIL = env('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
SERVER_EMAIL_PORT = '587'

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')
EMAIL_HOST_USER = env('EMAIL_USER')
EMAIL_PORT = 587
EMAIL_NOTIFY = True

MSG_PREFIX = 'MH'

# Anymail with Mailgun
#INSTALLED_APPS += ("anymail", )
#ANYMAIL = {
#    "MAILGUN_API_KEY": env('DJANGO_MAILGUN_API_KEY'),
#    "MAILGUN_SENDER_DOMAIN": env('MAILGUN_SENDER_DOMAIN')
#}
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader', [
        'django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader', ]),
]

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------

# Use the Heroku-style specification
# Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
DATABASES['default'] = env.db('DATABASE_URL')

# CACHING
# ------------------------------------------------------------------------------

REDIS_LOCATION = '{0}/{1}'.format(env('REDIS_URL', default='redis://127.0.0.1:6379'), 0)
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

PAYMENT_PROVIDERS['gocardless']['redirect_url'] = 'https://maidstone-hackspace.org.uk'

AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

AWS_S3_SECURE_URLS = True
AWS_S3_ENDPOINT_URL = 'https://ams3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATIC_URL = '%s/%s/%s/' % (AWS_S3_ENDPOINT_URL, AWS_STORAGE_BUCKET_NAME, AWS_LOCATION)

# COMPRESSOR
# ------------------------------------------------------------------------------
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_ENABLED = env.bool('COMPRESS_ENABLED', default=True)
