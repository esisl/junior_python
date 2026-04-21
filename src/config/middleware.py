# src/config/middleware.py
from django.contrib.auth.models import AnonymousUser
from utils.tokens import authenticate_token

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ', 1)[1].strip()
            token_obj = authenticate_token(token_key)
            if token_obj:
                request.user = token_obj.user
                request.auth = token_obj
                return self.get_response(request)

        request.user = AnonymousUser()
        request.auth = None
        return self.get_response(request)