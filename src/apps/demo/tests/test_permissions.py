import pytest
import json
from django.urls import reverse
from apps.accounts.models import User, Role, Token
from apps.rbac.models import PermissionRule

@pytest.mark.django_db
class TestArticlePermissions:
    def setup_method(self):
        self.role_user = Role.objects.create(name='test_user')
        self.role_admin = Role.objects.create(name='test_admin')
        
        self.user = User.objects.create_user(email='user@test.com', password='pass123', role=self.role_user)
        self.admin = User.objects.create_user(email='admin@test.com', password='pass123', role=self.role_admin, is_admin=True)
        
        self.user_token = Token.create_for_user(self.user)
        self.admin_token = Token.create_for_user(self.admin)
        
        PermissionRule.objects.create(role=self.role_user, resource='article', action='read', allowed=True)
        PermissionRule.objects.create(role=self.role_admin, resource='article', action='create', allowed=True)

    def _auth_header(self, token_key):
        return {'HTTP_AUTHORIZATION': f'Token {token_key}'}

    def test_user_can_read_articles(self, client):
        response = client.get(reverse('article-list'), **self._auth_header(self.user_token.key))
        assert response.status_code == 200
        data = json.loads(response.content)
        assert len(data) > 0

    def test_user_cannot_create_articles(self, client):
        response = client.post(
            reverse('article-create'), 
            json.dumps({'title': 'Hack'}), 
            content_type='application/json',
            **self._auth_header(self.user_token.key)
        )
        assert response.status_code == 403

    def test_admin_can_create_articles(self, client):
        response = client.post(
            reverse('article-create'), 
            json.dumps({'title': 'Admin Post'}), 
            content_type='application/json',
            **self._auth_header(self.admin_token.key)
        )
        assert response.status_code == 201
        data = json.loads(response.content)
        assert data['title'] == 'Admin Post'

    def test_unauthenticated_user_gets_401(self, client):
        response = client.get(reverse('article-list'))
        assert response.status_code == 401

@pytest.mark.django_db
class TestReportPermissions:
    def setup_method(self):
        self.role_user = Role.objects.create(name='report_tester')
        self.user = User.objects.create_user(email='reporter@test.com', password='pass123', role=self.role_user)
        self.token = Token.create_for_user(self.user)
        PermissionRule.objects.create(role=self.role_user, resource='report', action='read', allowed=False)

    def _auth_header(self, token_key):
        return {'HTTP_AUTHORIZATION': f'Token {token_key}'}

    def test_explicit_deny_works(self, client):
        response = client.get(reverse('report-list'), **self._auth_header(self.token.key))
        assert response.status_code == 403