# src/apps/accounts/permissions.py
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    """
    Проверяет только бизнес-права (RBAC).
    Аутентификация обрабатывается отдельно через IsAuthenticated.
    """
    def has_permission(self, request, view):
        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        
        if not resource or not action:
            raise PermissionDenied('Internal server error: permission resource/action not configured.')
        
        if not check_permission(request.user, resource, action):
            raise PermissionDenied('You do not have permission to perform this action.')
        
        return True