from rest_framework import permissions

class UnauthenticatedPermission(permissions.BasePermission):
    """
    Global permission check for the application.
    """
    def __init__(self, methods):
        self.methods = methods

    def has_permission(self, request, view):
        if request.method in self.methods:
            return True
        return False

class StaffAuthenticatedPermission(permissions.BasePermission):
    """
    Global permission check for the application.
    """

    def has_permission(self, request, view):
        return request.user.is_staff

class AdminAuthenticatedPermission(permissions.BasePermission):
    """
    Global permission check for the application.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser