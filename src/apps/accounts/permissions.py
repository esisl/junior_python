# src/apps/accounts/permissions.py
from rest_framework import permissions
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  # DRF -> 401
            
        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        
        if not resource or not action:
            return False  # Ошибка конфигурации View -> 403
            
        return check_permission(request.user, resource, action)