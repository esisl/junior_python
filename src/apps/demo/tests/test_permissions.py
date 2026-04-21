# src/apps/demo/tests/test_permissions.py
import pytest
import logging
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User, Role, Token
from apps.rbac.models import PermissionRule

pytestmark = pytest.mark.django_db
logger = logging.getLogger(__name__)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_rbac(db):
    """Фикстура с явной зависимостью от db для корректных транзакций"""
    role_user = Role.objects.create(name='test_user')
    role_admin = Role.objects.create(name='test_admin')
    
    user = User.objects.create_user(email='user@test.com', password='pass123', role=role_user)
    admin = User.objects.create_user(email='admin@test.com', password='pass123', role=role_admin, is_admin=True)
    
    user_token = Token.create_for_user(user)
    admin_token = Token.create_for_user(admin)
    
    # Создаем правила
    PermissionRule.objects.create(role=role_user, resource='article', action='read', allowed=True)
    PermissionRule.objects.create(role=role_admin, resource='article', action='create', allowed=True)
    
    return {'user': user, 'admin': admin, 'user_token': user_token, 'admin_token': admin_token}

class TestArticlePermissions:
    def test_user_can_read_articles(self, api_client, setup_rbac):
        # force_authenticate гарантирует, что в запросе будет валидный user
        api_client.force_authenticate(user=setup_rbac['user'], token=setup_rbac['user_token'])
        
        logger.info(">>> Running test_user_can_read_articles")
        response = api_client.get(reverse('article-list'))
        
        # Если упало здесь - смотрим логи выше, почему check_permission вернул False
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.data}"
        assert len(response.data) > 0

    def test_user_cannot_create_articles(self, api_client, setup_rbac):
        api_client.force_authenticate(user=setup_rbac['user'], token=setup_rbac['user_token'])
        response = api_client.post(reverse('article-create'), {'title': 'Hack'})
        assert response.status_code == 403

    def test_admin_can_create_articles(self, api_client, setup_rbac):
        api_client.force_authenticate(user=setup_rbac['admin'], token=setup_rbac['admin_token'])
        response = api_client.post(reverse('article-create'), {'title': 'Admin Post'})
        assert response.status_code == 201
        assert response.data['title'] == 'Admin Post'

    def test_unauthenticated_user_gets_401(self, api_client):
        # Не делаем force_authenticate
        response = api_client.get(reverse('article-list'))
        # DRF должен вернуть 401, если user is Anonymous
        assert response.status_code == 401

class TestReportPermissions:
    def test_explicit_deny_works(self, api_client, db):
        role_user = Role.objects.create(name='report_tester')
        user = User.objects.create_user(email='reporter@test.com', password='pass123', role=role_user)
        token = Token.create_for_user(user)
        # Явный запрет
        PermissionRule.objects.create(role=role_user, resource='report', action='read', allowed=False)
        
        api_client.force_authenticate(user=user, token=token)
        response = api_client.get(reverse('report-list'))
        assert response.status_code == 403