import pytest
from apps.accounts.models import User, Role
from apps.accounts.services import register_user, authenticate_user, soft_delete_user
from apps.accounts.exceptions import UserAlreadyExistsError, InvalidCredentialsError

@pytest.mark.django_db
def test_register_and_login():
    user = register_user(email="test@example.com", password="StrongPass123!")
    assert User.objects.filter(email="test@example.com").exists()
    
    result = authenticate_user("test@example.com", "StrongPass123!")
    assert "token" in result
    assert result["user_id"] == user.id

@pytest.mark.django_db
def test_duplicate_registration():
    register_user(email="dup@example.com", password="Pass1234!")
    with pytest.raises(UserAlreadyExistsError):
        register_user(email="dup@example.com", password="Pass1234!")

@pytest.mark.django_db
def test_soft_delete():
    user = register_user(email="del@example.com", password="Pass1234!")
    soft_delete_user(user)
    
    user.refresh_from_db()
    assert user.is_active is False
    
    with pytest.raises(InvalidCredentialsError):
        authenticate_user("del@example.com", "Pass1234!")