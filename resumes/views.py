from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Resume
from .serializers import ResumeSerializer



class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate the resume with the logged-in job seeker
        if self.request.user.role == 'job_seeker':
            job_seeker = self.request.user.job_seeker
            serializer.save(job_seeker=job_seeker)
        else:
            raise PermissionDenied("Only job seekers can upload resumes.")

    def get_queryset(self):
        # Restrict users to only access their own resumes
        if self.request.user.role == 'job_seeker':
            return Resume.objects.filter(job_seeker=self.request.user.job_seeker)
        else:
            return Resume.objects.none()