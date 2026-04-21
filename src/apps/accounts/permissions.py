# src/apps/accounts/permissions.py
from rest_framework import permissions
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    """
    Проверяет права через RBAC-сервис.
    Ожидает, что в view заданы атрибуты:
      - resource: str (например, 'article')
      - action: str (например, 'read')
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        
        if not resource or not action:
            # Если view не настроил атрибуты - запрещаем доступ (защита от ошибок разработчика)
            return False
        
        return check_permission(request.user, resource, action)