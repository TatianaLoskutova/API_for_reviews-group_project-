from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import CustomUser


class IsAuthenticatedAuthorModeratoAdminOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее доступ к действиям в зависимости от роли пользователя.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role in (
                CustomUser.Role.MODERATOR,
                CustomUser.Role.ADMIN,
            )
        )


class IsAuthorOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее доступ к действиям в зависимости
    от авторства и роли пользователя.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == CustomUser.Role.ADMIN
        )
