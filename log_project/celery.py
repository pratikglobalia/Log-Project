from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'log_project.settings')

app = Celery('log_project')

app.conf.beat_schedule = {
    'send_mail_to_user': {
        'task': 'find_index.tasks.send_mail_to_user',
        'schedule': crontab(minute='*/1'),
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')