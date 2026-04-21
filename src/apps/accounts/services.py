# src/apps/accounts/services.py
from django.contrib.auth.hashers import check_password
from apps.accounts.models import User, Token
from apps.accounts.exceptions import (
    UserAlreadyExistsError, InvalidCredentialsError, ProfileDeletionError
)

def register_user(email: str, password: str, **extra_fields) -> User:
    if User.objects.filter(email=email).exists():
        raise UserAlreadyExistsError(f"User with email {email} already exists")
    
    # Используем кастомный менеджер, который корректно хеширует пароль
    return User.objects.create_user(email=email, password=password, **extra_fields)

def authenticate_user(email: str, password: str) -> dict:
    user = User.objects.filter(email=email, is_active=True).select_related('role').first()
    
    # check_password сравнивает ввод с хешем в БД
    if not user or not check_password(password, user.password):
        raise InvalidCredentialsError("Invalid email or password")
    
    # Вызываем classmethod напрямую через класс Token
    token = Token.create_for_user(user)
    
    return {
        "token": token.key, 
        "user_id": user.id, 
        "role": user.role.name if user.role else None
    }

def logout_user(token_key: str) -> None:
    Token.objects.filter(key=token_key).update(is_revoked=True)

def soft_delete_user(user: User) -> None:
    if not user.is_active:
        raise ProfileDeletionError("Account is already deactivated")
    user.is_active = False
    # Аннулируем все токены пользователя при "удалении"
    user.tokens.update(is_revoked=True)
    user.save()