from __future__ import unicode_literals, absolute_import

from celery.schedules import crontab

from shipper.tasks import loadfileactiveusers, sendfile, cleanfolder
import os
from celery import Celery, chain

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.beat_schedule = {
    'users_report':{
        'task':'project.Celery.reportgenerator',
        'schedule':crontab(hour=8, minute=30,)
    }
}
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



@app.task(bind=True)
def test_tas(self):
    print(self.request)\

@app.task(bind=True)
def reportgenerator(self):
    chain(loadfileactiveusers.s(), sendfile.s(), cleanfolder.s())()
