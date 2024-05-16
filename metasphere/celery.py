from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metasphere.settings")

app = Celery("metasphere")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "archive-expired-stories-every-hour": {
        "task": "metasphere.apps.stories.tasks.archive_expired_stories",
        "schedule": crontab(minute=0, hour="*"),
    },
}
