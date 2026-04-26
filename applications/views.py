from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsJobSeekerOrEmployer
from analytics.utils import track_job_application
from .tasks import send_application_creation_email
from utils.async_handler import run_task



class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobSeekerOrEmployer]

    def perform_create(self, serializer):
        user = self.request.user

        # Automatically associate the application with the logged-in job seeker
        if hasattr(user, 'job_seeker'):
            job = serializer.validated_data.get('job')
            # Check if the user has already applied for this job
            if Application.objects.filter(job_seeker=user.job_seeker, job=job).exists():
                raise ValidationError("You have already applied for this job.")
            
            application = serializer.save(job_seeker=user.job_seeker)

            # Track the job application
            track_job_application(application.job)

            # Notify user of job creation asynchronously
            run_task(send_application_creation_email, user.email)

        else:
            raise PermissionDenied("Job Seeker profile does not exist for this user.")

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Application.objects.none()
        
        # Restrict users to only access their own applications
        user = self.request.user

        if user.role == 'job_seeker':
            if hasattr(user, 'job_seeker'):
                return Application.objects.filter(job_seeker=user.job_seeker)
            else:
                return Application.objects.none()
        
        elif user.role == 'employer':
            if hasattr(user, 'employer'):
                return Application.objects.filter(job__employer=user.employer)
            else:
                return Application.objects.none()
    
        else:
            return Application.objects.none()
        
    def perform_update(self, serializer):
        user = self.request.user

        if user.role == 'job_seeker' and 'status' in self.request.data:
            raise PermissionDenied("You do not have the permission to update application status.")
        
        serializer.save()

    def get_serializer_context(self):
        """Add request to serializer context for building absolute URLs"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
