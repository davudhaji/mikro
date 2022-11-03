from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mikrokridit.settings')

app = Celery('mikrokridit')

# Optional configuration, see the application user guide.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

REDIS_CONNECTION = '{protocol}://{username}:{password}@{host}:{port}'.format(
    protocol=os.environ.get('REDIS_PROTOCOL', 'redis'),
    username=os.environ.get('REDIS_USER', ''),
    password=os.environ.get('REDIS_PASSWORD', ''),
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=os.environ.get('REDIS_PORT', '6379'),
)
import mkridit.tasks
CELERY_CONFIG = dict(
    BROKER_URL='{redis}/1'.format(redis=REDIS_CONNECTION),
    CELERY_BEAT_SCHEDULE={
        "check_endpoints": {
            "task": "mkridit.tasks.check_endpoints",
            "schedule": crontab(minute=0, hour='*/8')
        },
        "send_email": {
            "task": "mkridit.tasks.send_email",
            "schedule": crontab(minute=0, hour='*/24')
        }
    },
    
    

    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_IGNORE_RESULT=True,
    CELERY_ACCEPT_CONTENT=['application/json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE = 'Asia/Baku'
)

app.conf.update(**CELERY_CONFIG)

app.conf.timezone = 'UTC'

# if __name__ == '__main__':
#     app.start()