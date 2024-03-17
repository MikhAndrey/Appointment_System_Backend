from django.conf import LazySettings
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

settings = LazySettings()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        authenticator = JWTAuthentication()
        response = authenticator.authenticate(request)
        if response is not None:
            user, token = response
            request.user = user
        else:
            return Response('Unauthorized', status=401)
