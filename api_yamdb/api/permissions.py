from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsAuthorOrModeratorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        request_user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or (request_user.is_authenticated
                and (request_user.is_moderator or request_user.is_admin)
                )
        )


class IsAdminOrReadOnly(IsAdmin):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )
