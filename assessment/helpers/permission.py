from rest_framework import permissions
from rest_framework.request import Request

class AllowedUserPermission(permissions.BasePermission):
    """
    Global permission check for the application.
    """
    def __init__(self, methods, permissions_class):
        self.methods = methods
        self.permissions_class = permissions_class

    def has_permission(self, request, view):
        if request.method in self.methods:
            return True
        return self.permissions_class.has_permission(self, request, view)

class StaffAuthenticatedPermission(permissions.BasePermission):
    """
    Global permission check for the application.
    """

    def has_permission(self, request, view):
        return (request.user.is_staff or request.user.is_superuser)

class AdminAuthenticatedPermission(permissions.BasePermission):
    """
    Global permission check for the application.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser
