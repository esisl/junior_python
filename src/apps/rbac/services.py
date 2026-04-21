# src/apps/rbac/services.py
from apps.rbac.models import PermissionRule
from apps.accounts.models import User

def check_permission(user: User, resource: str, action: str) -> bool:
    """
    Проверяет, имеет ли пользователь право выполнять действие над ресурсом.
    Логика:
    1. is_admin -> всегда разрешено
    2. is_active=False -> всегда запрещено
    3. Нет роли -> запрещено
    4. Ищем правило для роли+ресурс+действие. Если найдено -> возвращаем allowed.
    5. Правило не найдено -> запрещено (secure by default).
    """
    if not user or not user.is_active:
        return False
    
    if user.is_admin:
        return True
    
    if not user.role:
        return False
    
    # Ищем правило. При 1 роли на пользователя достаточно первого совпадения.
    rule = PermissionRule.objects.filter(
        role=user.role,
        resource=resource,
        action=action
    ).first()
    
    return rule.allowed if rule else False