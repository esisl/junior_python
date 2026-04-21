import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.accounts.models import User, Role
from apps.rbac.models import PermissionRule
from django.contrib.auth.hashers import make_password

def seed():
    # Роли
    role_admin, _ = Role.objects.get_or_create(name='admin')
    role_user, _ = Role.objects.get_or_create(name='user')

    # Правила
    rules = [
        (role_admin, 'article', 'create', True),
        (role_admin, 'article', 'read', True),
        (role_admin, 'article', 'update', True),
        (role_admin, 'article', 'delete', True),
        (role_admin, 'report', 'read', True),
        (role_user, 'article', 'read', True),
        (role_user, 'report', 'read', False), # Явный запрет
    ]
    
    for r, res, act, allowed in rules:
        PermissionRule.objects.update_or_create(
            role=r, resource=res, action=act, defaults={'allowed': allowed}
        )

    # Пользователи
    admin_user, _ = User.objects.get_or_create(email='admin@test.com', defaults={
        'password': make_password('admin123'), 'is_admin': True, 'role': role_admin
    })
    regular_user, _ = User.objects.get_or_create(email='user@test.com', defaults={
        'password': make_password('user123'), 'is_admin': False, 'role': role_user
    })

    print("✅ Seed completed. Users: admin@test.com / user@test.com (password: admin123 / user123)")

if __name__ == '__main__':
    seed()