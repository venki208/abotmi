from __future__ import absolute_import

import os

from celery import Celery
from reia import celeryconfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reia.settings-production')
app = Celery('reia')

from django.conf import settings

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.config_from_object('reia:celeryconfig')
