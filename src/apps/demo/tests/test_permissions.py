# src/apps/demo/tests/test_permissions.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import User, Role, Token
from apps.rbac.models import PermissionRule

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_data(db):
    """Фикстура создаёт роли, пользователей, токены и правила"""
    role_user = Role.objects.create(name='test_user')
    role_admin = Role.objects.create(name='test_admin')
    
    user = User.objects.create_user(email='user@test.com', password='pass123', role=role_user)
    admin = User.objects.create_user(email='admin@test.com', password='pass123', role=role_admin, is_admin=True)
    
    user_token = Token.create_for_user(user)
    admin_token = Token.create_for_user(admin)
    
    PermissionRule.objects.create(role=role_user, resource='article', action='read', allowed=True)
    PermissionRule.objects.create(role=role_admin, resource='article', action='create', allowed=True)
    
    return {
        'user': user, 'admin': admin,
        'user_token': user_token, 'admin_token': admin_token
    }

@pytest.mark.django_db
class TestArticlePermissions:
    def test_user_can_read_articles(self, api_client, test_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {test_data["user_token"].key}')
        response = api_client.get(reverse('article-list'))
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_user_cannot_create_articles(self, api_client, test_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {test_data["user_token"].key}')
        response = api_client.post(reverse('article-create'), {'title': 'Hack'})
        assert response.status_code == 403

    def test_admin_can_create_articles(self, api_client, test_data):
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {test_data["admin_token"].key}')
        response = api_client.post(reverse('article-create'), {'title': 'Admin Post'})
        assert response.status_code == 201
        assert response.data['title'] == 'Admin Post'

    def test_unauthenticated_user_gets_401(self, api_client):
        response = api_client.get(reverse('article-list'))
        assert response.status_code == 401

@pytest.mark.django_db
class TestReportPermissions:
    def test_explicit_deny_works(self, api_client, db):
        role_user = Role.objects.create(name='report_tester')
        user = User.objects.create_user(email='reporter@test.com', password='pass123', role=role_user)
        token = Token.create_for_user(user)
        PermissionRule.objects.create(role=role_user, resource='report', action='read', allowed=False)
        
        api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = api_client.get(reverse('report-list'))
        assert response.status_code == 403