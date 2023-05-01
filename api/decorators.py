from functools import wraps
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from oauth2_provider.models import AccessToken
from datetime import datetime

def func_token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Get token value from cookies  
        # cookie_header = request.COOKIES.get('oauth_token')
        # cookie_header= "oauth_token=9gpFoXxkXo0QenFWYbHrC4B13vm1iL;"
        # cookie_parts = cookie_header.split('=')  # ['oauth_token', 'hzUsEXabgyc8EgPAgEoM78ggBRef0R;']
        # token = cookie_parts[1].strip(';') #  'hzUsEXabgyc8EgPAgEoM78ggBRef0R'

        auth_header = request.headers.get("Authorization", "").split()
        if not auth_header or auth_header[0].lower() != "bearer":
            return JsonResponse(
                {"error": "Invalid token header. No credentials provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # # get the token string
        token= auth_header[1]
        if not token:
            # Token cookie not found, handle error
            return JsonResponse({"error":"token not found"}, status=status.HTTP_404_NOT_FOUND)
           
        try:
            access_token = AccessToken.objects.get(token=token)
        except AccessToken.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid access token. Token not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the token has expired
        expires_at = access_token.expires
        now = datetime.utcnow().replace(tzinfo=expires_at.tzinfo)
        if expires_at < now:
            return JsonResponse(
                {"error": "The access token has expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        return view_func(request, *args, **kwargs)
    return wrapper


def token_required(func):
    @wraps(func)
    def wrapper(self,request, *args, **kwargs):
        # when using class method we need to pass self argument as first
        # get the token from the Authorization header
        auth_header = request.headers.get("Authorization", "").split()
        if not auth_header or auth_header[0].lower() != "bearer":
            return JsonResponse(
                {"error": "Invalid token header. No credentials provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        #  get the token string
        token= auth_header[1]
        if not token:
            # Token cookie not found, handle error
            return JsonResponse({"error":"token not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            access_token = AccessToken.objects.get(token=token)
        except AccessToken.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid access token. Token not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the token has expired
        expires_at = access_token.expires
        now = datetime.utcnow().replace(tzinfo=expires_at.tzinfo)
        if expires_at < now:
            return JsonResponse(
                {"error": "The access token has expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        # Pass token value to view function
        return func(self,request,*args, **kwargs)
    return wrapper
