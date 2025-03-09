from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Analytics
from .serializers import AnalyticsSerializer



class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AnalyticsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # If user is a job seeker, return analytics for their applications
        if user.role == 'job_seeker':
            if hasattr(user, 'job_seeker'):
                # Get all jobs the job seeker has applied to
                applications = user.job_seeker.applications.all()
                job_ids = [application.job_id for application in applications]
                # Get analytics for those jobs
                return Analytics.objects.filter(job_id__in=job_ids)
            else:
                return Analytics.objects.none()

        # If user is an employer, return analytics for their job postings
        elif user.role == 'employer':
            if hasattr(user, 'employer'):
                # Get all jobs posted by the employer
                jobs = user.employer.jobs.all()
                job_ids = [job.job_id for job in jobs]
                # Get analytics for those jobs
                return Analytics.objects.filter(job_id__in=job_ids)
            else:
                return Analytics.objects.none()

        else:
            return Analytics.objects.none()

