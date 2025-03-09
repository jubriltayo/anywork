from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsJobSeeker, IsEmployer
from analytics.utils import track_job_application
from .tasks import send_application_creation_email



class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker, IsEmployer]

    def perform_create(self, serializer):
        user = self.request.user
        print(user.email)

        # Automatically associate the application with the logged-in job seeker
        if hasattr(user, 'job_seeker'):
            application = serializer.save(job_seeker=user.job_seeker)

            # Track the job application
            track_job_application(application.job)

            # Notify user of job creation asynchronously
            send_application_creation_email.delay(user.email)

        else:
            raise PermissionDenied("Job Seeker profile does not exist for this user.")

    def get_queryset(self):
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
