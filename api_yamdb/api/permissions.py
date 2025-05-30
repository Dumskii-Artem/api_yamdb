from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and  request.user.is_admin

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

class IsAuthorOrModeratorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS or
            obj.author == request.user or
            request.user.is_moderator or
            request.user.is_admin
        )