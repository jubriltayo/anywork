import os
from celery import Celery


# Set default Django settings module for the celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# create the celery app
app = Celery('applications')

# Load configuration from settings 
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
