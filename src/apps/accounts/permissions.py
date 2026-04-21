from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    """
    Объединяет проверку аутентификации и RBAC-прав.
    Явно возвращает 401 для анонимов и 403 при отсутствии прав.
    """
    def has_permission(self, request, view):
        # 1. Проверка аутентификации -> 401
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated('Authentication credentials were not provided.')

        # 2. Валидация конфигурации View -> 403 при ошибке настройки
        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)
        if not resource or not action:
            raise PermissionDenied('Internal server error: permission resource/action not configured.')

        # 3. Проверка бизнес-прав через RBAC -> 403 при отказе
        if not check_permission(request.user, resource, action):
            raise PermissionDenied('You do not have permission to perform this action.')

        return True