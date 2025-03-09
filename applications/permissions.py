from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied



class IsJobSeeker(permissions.BasePermission):
    """
    Permission to only allow job seekers to create applications.
    """
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.role != 'job_seeker':
            raise PermissionDenied("Only job seekers can apply for jobs.")
        return True


class IsEmployer(permissions.BasePermission):
    """
    Permission to only allow employers to update application status.
    """
    def has_permission(self, request, view):
        if request.method in ['PUT', 'PATCH'] and request.user.role != 'employer':
            raise PermissionDenied("Only employers can update application status.")
        return True
