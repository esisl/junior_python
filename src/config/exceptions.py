# src/config/exceptions.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from apps.accounts.exceptions import AccountError

def custom_exception_handler(exc, context):
    # 1. Явно форсируем 401 для ошибок аутентификации
    if isinstance(exc, NotAuthenticated):
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # 2. Бизнес-ошибки (регистрация, токены и т.д.)
    if isinstance(exc, AccountError):
        return Response(
            {"detail": str(exc), "code": exc.__class__.__name__},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 3. Всё остальное делегируем стандартному обработчику DRF
    return exception_handler(exc, context)