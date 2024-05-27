import os
from celery import Celery
from celery.schedules import crontab

# Celery settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Setting up a task for celery-beat
app.conf.beat_schedule = {
    'fetch-currency-rates-every-5-minutes': {
        'task': 'currency.tasks.fetch_currency_rates',
        'schedule': crontab(minute='*/5'),
    },
}
