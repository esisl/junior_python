from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from utils.tokens import authenticate_token
import re

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        match = re.match(r'^Token\s(.+)$', auth_header)
        if match:
            token_key = match.group(1)
            token_obj = authenticate_token(token_key)
            if token_obj:
                request.user = token_obj.user
                request.auth = token_obj
                return
        # Если токен невалиден или отсутствует, DRF permissions обработают это как 401
        request.user = None
        request.auth = None