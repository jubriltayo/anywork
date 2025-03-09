from rest_framework import permissions


class IsEmployer(permissions.BasePermission):
    """
    Permission to only allow to CUD job-related data
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # SAFE METHODS = GET, HEAD, OPTIONS
            return True
        return request.user.role == 'employer'
