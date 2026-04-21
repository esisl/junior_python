# src/apps/accounts/permissions.py
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    def has_permission(self, request, view):
        # 1. Сначала проверяем аутентификацию -> 401
        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed('Authentication credentials were not provided or token is invalid.')
        
        # 2. Проверяем конфигурацию вью
        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        
        if not resource or not action:
            raise PermissionDenied('Internal server error: permission resource/action not configured.')
        
        # 3. Проверяем права через RBAC -> 403 при отказе
        if not check_permission(request.user, resource, action):
            raise PermissionDenied('You do not have permission to perform this action.')
        
        return True