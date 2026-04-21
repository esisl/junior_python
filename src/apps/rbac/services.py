# src/apps/rbac/services.py
import logging
from apps.rbac.models import PermissionRule

logger = logging.getLogger(__name__)

def check_permission(user, resource: str, action: str) -> bool:
    # 1. Базовые проверки
    if not user or not hasattr(user, 'is_active') or not user.is_active:
        logger.warning(f"Permission DENIED: User {user} is inactive or invalid")
        return False
    
    # 2. Суперпользователь
    if getattr(user, 'is_admin', False):
        logger.info(f"Permission ALLOWED: User {user} is admin")
        return True
    
    # 3. Проверка роли
    user_role = getattr(user, 'role', None)
    if not user_role:
        logger.warning(f"Permission DENIED: User {user} has no role")
        return False
    
    # 4. Поиск правила (с логированием запроса)
    logger.info(f"Checking rule: role={user_role.name}, res={resource}, act={action}")
    
    rule = PermissionRule.objects.filter(
        role=user_role,
        resource=resource,
        action=action
    ).first()
    
    if rule:
        logger.info(f"Rule found: allowed={rule.allowed}")
        return rule.allowed
    else:
        logger.warning(f"Rule NOT FOUND: {user_role.name} -> {action} {resource}")
        return False  # Secure by default