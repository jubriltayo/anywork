from django.utils import timezone
from django.db import transaction
from django.db.models import F
from .models import Analytics

def track_job_view(job):
    """
    Track a job view by atomically incrementing the view count.
    Uses database-level atomic operations to prevent race conditions.
    """
    try:
        today = timezone.now().date()
        
        with transaction.atomic():
            # Atomically update or create the analytics record
            analytics, created = Analytics.objects.select_for_update().get_or_create(
                job=job,
                date=today,
                defaults={'views': 1}
            )
            
            if not created:
                # Use F() expression for atomic increment at database level
                Analytics.objects.filter(
                    analytics_id=analytics.analytics_id
                ).update(views=F('views') + 1)
                
    except Exception as e:
        print(f"Error tracking job view: {e}")

def track_job_application(job):
    """
    Track a job application by atomically incrementing the application count.
    Uses database-level atomic operations to prevent race conditions.
    """
    try:
        today = timezone.now().date()
        
        with transaction.atomic():
            # Atomically update or create the analytics record
            analytics, created = Analytics.objects.select_for_update().get_or_create(
                job=job,
                date=today,
                defaults={'applications': 1}
            )
            
            if not created:
                # Use F() expression for atomic increment at database level
                Analytics.objects.filter(
                    analytics_id=analytics.analytics_id
                ).update(applications=F('applications') + 1)
                
    except Exception as e:
        print(f"Error tracking job application: {e}")