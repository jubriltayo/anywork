from rest_framework import permissions

class IsJobSeekerOrEmployer(permissions.BasePermission):
    """
    Permission to allow both job seekers and employers with different access levels.
    """
    def has_permission(self, request, view):
        return request.user.role in ['job_seeker', 'employer']
