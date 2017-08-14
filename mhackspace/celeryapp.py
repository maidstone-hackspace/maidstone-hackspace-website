from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
# from django.apps import apps, AppConfig

# if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    # ;os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

from django.conf import settings
app = Celery('mhackspace')
# app.config_from_object(settings)
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: ['mhackspace.base'])

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
