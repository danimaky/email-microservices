from __future__ import unicode_literals, absolute_import
from celery.schedules import crontab
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.beat_schedule = {
    'users-report-every-5-minutes': {
        'task': 'shipper.tasks.reportgenerator',
        'schedule': crontab(hour=8),
        'args': (),
        'kwargs': {}
    }
}
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def test_tas(self):
    print(self.request)
