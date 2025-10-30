from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, CategoryViewSet, JobViewSet, EmployerJobViewSet


router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'jobs', JobViewSet, basename='job')
router.register('employer/jobs', EmployerJobViewSet, basename='employer-job')


urlpatterns = [
    path('', include(router.urls)),
]