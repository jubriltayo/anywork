from rest_framework import permissions

class IsEmployerReadWrite(permissions.BasePermission):
    """
    Permission that only allows employers to perform any actions (read/write)
    Used for employer-specific endpoints like /employer/jobs/
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employer'

    def has_object_permission(self, request, view, obj):
        # For employer-specific endpoints, they can only access their own objects
        return obj.employer.user == request.user


class IsEmployerWriteOnly(permissions.BasePermission):
    """
    Permission that allows everyone to read, but only employers to write
    Used for public job browsing endpoints like /jobs/
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True  # Anyone can view
        return request.user.is_authenticated and request.user.role == 'employer'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True  # Anyone can view
        # Only allow employers to modify their own job postings
        return obj.employer.user == request.user