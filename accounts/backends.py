from django.contrib.auth.hashers import check_password
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions
from rest_framework.response import Response
from .models import DiscordUser
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.backends import ModelBackend

import datetime

from .utils import get_user

class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            raise exceptions.AuthenticationFailed('Authentication header not found.')

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('In authentication header prefix or token not found.')

        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Authentication header is bigger.')

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            raise exceptions.AuthenticationFailed('Token prefix error.')
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            msg = 'Token expired.'
            raise exceptions.AuthenticationFailed(msg)
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)


        try:
            user = DiscordUser.objects.get(id=payload['id'])
        except DiscordUser.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        if payload['ip'] != request.META['REMOTE_ADDR']:
            raise exceptions.AuthenticationFailed("Invalid ip verification.")
        return (user, token)

class JWTGetModAuthentication(JWTAuthentication):
    authentication_header_prefix = 'Mod'


def authenticate(token):
    discord_user = get_user(token)
    discord_id = discord_user['id']
    discord_username = discord_user['username'] + "#" + discord_user['discriminator']
    try:
        user = DiscordUser.objects.get(discord_id=discord_id)
    except DiscordUser.DoesNotExist:
        user = DiscordUser()
        user.discord_id = discord_id
        user.username = discord_username
        user.save()
    return user
