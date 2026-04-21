# src/apps/demo/tests/test_permissions.py
import pytest
from django.urls import reverse
from apps.accounts.models import User, Role, Token
from apps.rbac.models import PermissionRule

@pytest.mark.django_db
class TestArticlePermissions:
    def setup_method(self):
        # Создаём роли и пользователей для тестов
        self.role_user = Role.objects.create(name='test_user')
        self.role_admin = Role.objects.create(name='test_admin')
        
        self.user = User.objects.create_user(email='user@test.com', password='pass123', role=self.role_user)
        self.admin = User.objects.create_user(email='admin@test.com', password='pass123', role=self.role_admin, is_admin=True)
        
        self.user_token = Token.create_for_user(self.user)
        self.admin_token = Token.create_for_user(self.admin)
        
        # Базовое правило: обычный пользователь может читать статьи
        PermissionRule.objects.create(role=self.role_user, resource='article', action='read', allowed=True)
        # Админ имеет все права через is_admin, правила не обязательны, но добавим для полноты
        PermissionRule.objects.create(role=self.role_admin, resource='article', action='create', allowed=True)

    def _auth_header(self, token_key):
        return {'HTTP_AUTHORIZATION': f'Token {token_key}'}

    def test_user_can_read_articles(self):
        response = self.client.get(reverse('article-list'), **self._auth_header(self.user_token.key))
        assert response.status_code == 200
        assert len(response.data) > 0

    def test_user_cannot_create_articles(self):
        response = self.client.post(reverse('article-create'), {'title': 'Hack'}, **self._auth_header(self.user_token.key))
        assert response.status_code == 403  # Forbidden

    def test_admin_can_create_articles(self):
        response = self.client.post(reverse('article-create'), {'title': 'Admin Post'}, **self._auth_header(self.admin_token.key))
        assert response.status_code == 201
        assert response.data['title'] == 'Admin Post'

    def test_unauthenticated_user_gets_401(self):
        response = self.client.get(reverse('article-list'))
        assert response.status_code == 401

@pytest.mark.django_db
class TestReportPermissions:
    def setup_method(self):
        self.role_user = Role.objects.create(name='report_tester')
        self.user = User.objects.create_user(email='reporter@test.com', password='pass123', role=self.role_user)
        self.token = Token.create_for_user(self.user)
        # Явно запрещаем доступ к отчётам
        PermissionRule.objects.create(role=self.role_user, resource='report', action='read', allowed=False)

    def _auth_header(self, token_key):
        return {'HTTP_AUTHORIZATION': f'Token {token_key}'}

    def test_explicit_deny_works(self):
        response = self.client.get(reverse('report-list'), **self._auth_header(self.token.key))
        assert response.status_code == 403  # Запрет из PermissionRule сработал