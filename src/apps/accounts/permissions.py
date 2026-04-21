# src/apps/accounts/permissions.py
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    """
    Проверяет только бизнес-права (RBAC) для УЖЕ аутентифицированных пользователей.
    Если пользователь не аутентифицирован — пропускаем проверку, 
    пусть за возврат 401 отвечает IsAuthenticated.
    """
    def has_permission(self, request, view):
        # Ключевая правка: если пользователь не аутентифицирован — возвращаем True
        if not request.user or not request.user.is_authenticated:
            return True
        
        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        
        if not resource or not action:
            raise PermissionDenied('Internal server error: permission resource/action not configured.')
        
        if not check_permission(request.user, resource, action):
            raise PermissionDenied('You do not have permission to perform this action.')
        
        return True