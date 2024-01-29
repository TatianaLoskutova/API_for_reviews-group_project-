from rest_framework.permissions import BasePermission

from .models import CustomUser


class IsSuperUserOrAdmin(BasePermission):
    """
    Permission для SUPERUSER или ADMIN.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == CustomUser.Role.ADMIN
                or request.user.is_superuser
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user.role == CustomUser.Role.ADMIN
                or request.user.is_superuser
            )
        )
