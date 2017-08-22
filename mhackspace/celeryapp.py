# from __future__ import absolute_import
import os
from django.conf import settings
from celery import Celery


if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('mhackspace')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.autodiscover_tasks(lambda: ['mhackspace.base'], related_name='tasks')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover
