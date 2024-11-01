from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
import os
import multiprocessing
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_planning.settings')
app = Celery('event_planning')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['event_planning_api'])


app.conf.beat_schedule = {
    'send_notifications': {
        'task': 'event_planning_api.tasks.send_event_notifications',
        'schedule': crontab(minute='*/1'),  
    },
}


app.conf.broker_url = 'redis://127.0.0.1:6379/0'  # Ensure this is set
app.conf.result_backend = 'redis://127.0.0.1:6379/0'  


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    app.start()