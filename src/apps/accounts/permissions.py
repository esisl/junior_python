# src/apps/accounts/permissions.py
from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    """
    Единая точка проверки: сначала аутентификация (401), затем RBAC-права (403).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()

        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        if not resource or not action:
            raise PermissionDenied('Internal server error: permission resource/action not configured.')

        if not check_permission(request.user, resource, action):
            raise PermissionDenied('You do not have permission to perform this action.')

        return True