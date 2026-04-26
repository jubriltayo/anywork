from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from applications.models import Application
from .models import Skill
from .serializers import SkillSerializer


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Skill.objects.none()
        
        user = self.request.user

        # If user is a job seeker, return skills associated with their profile
        if user.role == 'job_seeker':
            return Skill.objects.filter(user=user)

        # If user is an employer, return all skills of users who applied for their jobs
        elif user.role == 'employer':
            if hasattr(user, 'employer'):
                jobs = user.employer.jobs.all()
                applications = Application.objects.filter(job__in=jobs)
                users = applications.values_list('job_seeker__user', flat=True)
                # get all skills of job seekers who applied for their job
                return Skill.objects.filter(user__in=users).distinct()
            else:
                return Skill.objects.none()
            
        else:
            return Skill.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Only job seekers can create skills
        if user.role != 'job_seeker':
            raise PermissionDenied("Only job seekers can create skills.")
        serializer.save(user=user)

