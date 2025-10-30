from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .filters import JobFilter
from .models import Location, Category, Job
from .permissions import IsEmployerReadWrite, IsEmployerWriteOnly
from .serializers import LocationSerializer, CategorySerializer, JobSerializer
from analytics.utils import track_job_view



class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsEmployerReadWrite]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsEmployerReadWrite]


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for public job browsing.
    Returns all active jobs for everyone to read.
    """
    serializer_class = JobSerializer
    permission_classes = [IsEmployerWriteOnly]  # Updated permission
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description', 'location__city', 'category__name']

    def get_queryset(self):
        return Job.objects.filter(is_active=True)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'employer':
            raise PermissionDenied("Only employers can create jobs.")
        serializer.save(employer=user.employer)

    def retrieve(self, request, *args, **kwargs):
        job = self.get_object()
        track_job_view(job)
        return super().retrieve(request, *args, **kwargs)


class EmployerJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for employer to manage their own jobs.
    Returns only jobs created by the authenticated employer.
    """
    serializer_class = JobSerializer
    permission_classes = [IsEmployerReadWrite]
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'employer' and hasattr(user, 'employer'):
            return Job.objects.filter(employer=user.employer)
        return Job.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(employer=user.employer)

