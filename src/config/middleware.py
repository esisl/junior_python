# src/config/middleware.py
from django.contrib.auth.models import AnonymousUser
from utils.tokens import authenticate_token

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        user = AnonymousUser()
        auth_token = None

        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ', 1)[1].strip()
            try:
                token_obj = authenticate_token(token_key)
                if token_obj:
                    user = token_obj.user
                    auth_token = token_obj
            except Exception:
                # В production лучше логировать, но для теста просто игнорируем
                pass

        request.user = user
        request.auth = auth_token
        return self.get_response(request)