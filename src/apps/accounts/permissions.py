from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from apps.rbac.services import check_permission

class IsAllowedAction(permissions.BasePermission):
    def has_permission(self, request, view):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            raise AuthenticationFailed('Authentication credentials were not provided or token is invalid.')

        resource = getattr(view, 'resource', None)
        action = getattr(view, 'action', None)

        if not resource or not action:
            raise PermissionDenied('Internal server error: permission resource/action not configured.')

        if not check_permission(user, resource, action):
            raise PermissionDenied('You do not have permission to perform this action.')

        return True