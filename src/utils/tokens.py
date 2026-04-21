import secrets
from apps.accounts.models import Token

def generate_token() -> str:
    return secrets.token_urlsafe(48)

def authenticate_token(key: str) -> Token:
    try:
        token = Token.objects.select_related('user').get(key=key)
        if token.is_revoked:
            from apps.accounts.exceptions import TokenRevokedError
            raise TokenRevokedError("Token has been revoked")
        if not token.user.is_active:
            raise ValueError("User is inactive")
        return token
    except Token.DoesNotExist:
        return None