from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_accounts.settings')

app = Celery('django_accounts')
# ,broker="amqps://admin:ESAIASOXBCPPZKLM@sl-us-dal-9-portal.4.dblayer.com:20093/bmix_dal_yp_89fbe68a_95fe_43c6_a881_ecad79b8055a")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))