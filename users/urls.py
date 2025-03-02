from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserRegistrationView, LoginView, GoogleLoginView, JobSeekerViewSet, EmployerViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'jobseekers', JobSeekerViewSet, basename='jobseeker')
router.register(r'employers', EmployerViewSet, basename='employer')




urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', UserRegistrationView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login')
]

