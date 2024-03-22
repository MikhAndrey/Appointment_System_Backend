from django.conf import LazySettings
from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.response import Response

settings = LazySettings()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        excluded_urls = [reverse('token_obtain_pair'), reverse('token_refresh')]
        if request.path not in excluded_urls and "admin" not in request.path:
            try:
                authenticator = JWTAuthentication()
                response = authenticator.authenticate(request)
                if response is not None:
                    user, token = response
                    request.user = user
                else:
                    return JsonResponse(Response(message='Unauthorized').__dict__, status=401)
            except:
                return JsonResponse(Response(message='Unauthorized').__dict__, status=401)
