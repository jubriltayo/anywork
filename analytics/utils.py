from django.utils import timezone

from .models import Analytics



def track_job_view(job):
    """
    Track a job view by incrementing the view count in the Analytics model.
    """
    analytics, created = Analytics.objects.get_or_create(job=job, date=timezone.now().date())
    analytics.views += 1
    analytics.save()


def track_job_application(job):
    """
    Track a job application by incrementing the application count in the Analytics model.
    """
    analytics, created = Analytics.objects.get_or_create(job=job, date=timezone.now().date())
    analytics.applications += 1
    analytics.save()