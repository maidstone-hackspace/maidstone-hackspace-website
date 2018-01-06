# -*- coding: utf-8 -*-
"""
Django settings for Maidstone Hackspace project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import os
import time
import environ

# from spirit.settings import *
ROOT_DIR = environ.Path(__file__) - 3  # (mhackspace/config/settings/common.py - 3 = mhackspace/)
APPS_DIR = ROOT_DIR.path('mhackspace')

env = environ.Env()
env.read_env('%s/.env' % ROOT_DIR)

ST_TOPIC_PRIVATE_CATEGORY_PK = 1
ST_RATELIMIT_ENABLE = True
ST_RATELIMIT_CACHE_PREFIX = 'srl'
ST_RATELIMIT_CACHE = 'default'
ST_RATELIMIT_SKIP_TIMEOUT_CHECK = False
ST_NOTIFICATIONS_PER_PAGE = 20
ST_COMMENT_MAX_LEN = 3000
ST_MENTIONS_PER_COMMENT = 30
ST_DOUBLE_POST_THRESHOLD_MINUTES = 30
ST_YT_PAGINATOR_PAGE_RANGE = 3
ST_SEARCH_QUERY_MIN_LEN = 3
ST_USER_LAST_SEEN_THRESHOLD_MINUTES = 1
ST_PRIVATE_FORUM = False
ST_ALLOWED_UPLOAD_IMAGE_FORMAT = ('jpeg', 'png', 'gif')
ST_ALLOWED_URL_PROTOCOLS = {
    'http', 'https', 'mailto', 'ftp', 'ftps',
    'git', 'svn', 'magnet', 'irc', 'ircs'}

ST_UNICODE_SLUGS = True
ST_UNIQUE_EMAILS = True
ST_CASE_INSENSITIVE_EMAILS = True
ST_UPLOAD_IMAGE_ENABLED = True
ST_UPLOAD_FILE_ENABLED = True

# Tests helpers
ST_TESTS_RATELIMIT_NEVER_EXPIRE = False
ST_BASE_DIR = os.path.dirname(__file__)


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'search', 'whoosh_index'),
    },
}

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'crispy_forms',  # Form layouts
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    'allauth.socialaccount.providers.google',  # registration
    'allauth.socialaccount.providers.github',  # registration
    # 'allauth.socialaccount.providers.facebook',  # registration
    'whitenoise.runserver_nostatic',
    'stdimage',
    'rest_framework',
    'django_filters',
    'martor',
    'haystack',
    'djconfig',

    'corsheaders',

    'spirit.core',
    'spirit.admin',
    'spirit.search',

    'spirit.user',
    'spirit.user.admin',
    'spirit.user.auth',

    'spirit.category',
    'spirit.category.admin',

    'spirit.topic',
    'spirit.topic.admin',
    'spirit.topic.favorite',
    'spirit.topic.moderate',
    'spirit.topic.notification',
    'spirit.topic.poll',  # todo: remove in Spirit v0.6
    'spirit.topic.private',
    'spirit.topic.unread',

    'spirit.comment',
    'spirit.comment.bookmark',
    'spirit.comment.flag',
    'spirit.comment.flag.admin',
    'spirit.comment.history',
    'spirit.comment.like',
    'spirit.comment.poll',

    'django_nyt',
    'mptt',
    'sekizai',
    'sorl.thumbnail',
    'wiki',
    'wiki.plugins.attachments',
    'wiki.plugins.notifications',
    'wiki.plugins.images',
    'wiki.plugins.macros',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    # custom users app
    # Your stuff: custom apps go here
    'mhackspace.users.apps.UsersConfig',
    'mhackspace.base',
    'mhackspace.subscriptions',
    'mhackspace.feeds',
    'mhackspace.contact',
    'mhackspace.members',
    'mhackspace.blog',
    'mhackspace.core',
    'mhackspace.requests',
    'mhackspace.register',
    'mhackspace.rfid',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #fix for ip logging behind a proxy
    'x_forwarded_for.middleware.XForwardedForMiddleware',
    'djconfig.middleware.DjConfigMiddleware',

    'spirit.user.middleware.TimezoneMiddleware',
    'spirit.user.middleware.LastIPMiddleware',
    'spirit.user.middleware.LastSeenMiddleware',
    'spirit.user.middleware.ActiveUserMiddleware',
    'spirit.core.middleware.PrivateForumMiddleware',
)

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'mhackspace.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ("""Maidstone Hackspace""", 'support@maidstone-hackspace.org.uk'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///mhackspace'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                # Your stuff: custom template context processors go here
                'djconfig.context_processors.config',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
)
# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))
MARTOR_UPLOAD_PATH = 'images/uploads/{}'.format(time.strftime("%Y/%m/%d/"))
MARTOR_UPLOAD_URL = '/api/uploader/'  # change to local uploader
MARTOR_MARKDOWN_BASE_EMOJI_URL = '/static/images/emojis/'
MAX_IMAGE_UPLOAD_SIZE = 5242880  # 5MB


# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# PASSWORD HASHING
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'mhackspace.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'mhackspace.users.adapters.SocialAccountAdapter'
SOCIALACCOUNT_QUERY_EMAIL = True

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = 'users:redirect'
#LOGIN_URL = 'account_login'
WIKI_SIGNUP_URL = 'account_login'
#WIKI_EDITOR = 'wiki.editors.martor.Martor'
# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

# CELERY
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_IGNORE_RESULT = False
CELERY_REDIS_HOST = "redis"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
INSTALLED_APPS += ('django_celery_results', 'django_celery_beat',)
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# END CELERY

# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ("compressor", 'sass_processor',)
STATICFILES_FINDERS += ("compressor.finders.CompressorFinder", )

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = '^trustee/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------


PAYMENT_PROVIDERS = {
    'braintree': {
        'mode': env('PAYMENT_ENVIRONMENT'),
        'redirect_url': env('PAYMENT_REDIRECT_URL'),
        'credentials': {
            'merchant_id': env('BRAINTREE_MERCHANT_ID'),
            'public_key': env('BRAINTREE_PUBLIC_KEY'),
            'private_key': env('BRAINTREE_PRIVATE_KEY'),
        }
    },
    'paypal': {
        "mode": env('PAYMENT_ENVIRONMENT'),  # sandbox or live
        'redirect_url': env('PAYMENT_REDIRECT_URL'),
        'credentials': {
            "mode": "sandbox",  # sandbox or live
            "client_id": env('PAYPAL_CLIENT_ID'),
            "client_secret": env('PAYPAL_CLIENT_SECRET')}
        },
    'gocardless': {
        'environment': env('PAYMENT_ENVIRONMENT'),
        'redirect_url': env('PAYMENT_REDIRECT_URL'),
        'credentials': {
            'app_id': env('GOCARDLESS_APP_ID'),
            'app_secret': env('GOCARDLESS_APP_SECRET'),
            'access_token': env('GOCARDLESS_ACCESS_TOKEN'),
            'merchant_id': env('GOCARDLESS_MERCHANT_ID'),
        },
    }
}

SASS_PRECISION = 8

SASS_PROCESSOR_INCLUDE_DIRS = [
    str(APPS_DIR) + '/static/sass',
    str(ROOT_DIR) + '/node_modules',
]


SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_AUTO_INCLUDE = True

EMAIL_NOTIFY = True
EMAIL_SUPPORT = 'support@maidstone-hackspace.org.uk'
EMAIL_MAILING_LIST = 'maidstone-hackspace@googlegroups.com'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

# Deprecated need removing, sorl plugin still expects TEMPLATE_DEBUG so for now we need it just for this plugin
TEMPLATE_DEBUG = False
CORS_ORIGIN_WHITELIST = (
    'matrix.org',
    'vector.im',
    'riot.im'
)

MATRIX_USER=env('MATRIX_USERNAME')
MATRIX_PASSWORD=env('MATRIX_PASSWORD')
MATRIX_ROOM=env('MATRIX_ROOM')
MSG_PREFIX = 'MH'
X_FRAME_OPTIONS = 'SAMEORIGIN'
