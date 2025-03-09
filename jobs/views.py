from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .filters import JobFilter
from .models import Location, Category, Job
from .permissions import IsEmployer
from .serializers import LocationSerializer, CategorySerializer, JobSerializer
from analytics.utils import track_job_view



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsEmployer]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsEmployer]


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'location__city', 'category__name']

    def get_queryset(self):
        user = self.request.user

        # If user is a job seeker, return all active job postings
        if user.role == 'job_seeker':
            return Job.objects.filter(is_active=True)
        
        # If user is an employer, return only jobs they created
        elif user.role == 'employer':
            if hasattr(user, 'employer'):
                return Job.objects.filter(employer=user.employer)
            else:
                return Job.objects.none()
            
        else:
            return Job.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Only employers can create jobs
        if user.role != 'employer':
            raise PermissionDenied("Only employers can create jobs.")
        serializer.save(employer=user.employer)

    def retrieve(self, request, *args, **kwargs):
        # Override the default retrieve method to track job views as well
        job = self.get_object()

        track_job_view(job)

        return super().retrieve(request, *args, **kwargs)



