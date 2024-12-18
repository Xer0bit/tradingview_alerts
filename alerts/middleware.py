from django.http import JsonResponse
from utils.security import validate_token

class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Temporarily allow all requests
        return self.get_response(request)
