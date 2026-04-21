from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from apps.accounts.exceptions import AccountError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if isinstance(exc, AccountError):
        return Response(
            {"detail": str(exc), "code": exc.__class__.__name__},
            status=status.HTTP_400_BAD_REQUEST
        )
    return response