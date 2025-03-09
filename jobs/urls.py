from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, CategoryViewSet, JobViewSet


router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]