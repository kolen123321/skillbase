from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import SecretCode, DiscordUser
from .models import HaveMod
import datetime, jwt, time
from skillbase_api import settings

from accounts.backends import JWTAuthentication

from asgiref.sync import sync_to_async

class ModsView(APIView):

    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        user_mods = HaveMod.objects.filter(user=user)
        if not user_mods.exists():
            user_mods = HaveMod()
            user_mods.user = user
            user_mods.save()
        else:
            user_mods = HaveMod.objects.get(user=user)
        mods = {}
        for mod in user_mods.mods.all():
            mods[mod.name] = f"http://{request.META['HTTP_HOST']}/mods/?mod={mod.name}"
        mods['access_token'] = {
            'token': jwt.encode({
                'id': user.id,
                'exp': time.time() + 60
            }, key=settings.SECRET_KEY, algorithm="HS256"),
            'type': 'Mod'
        }
        return Response(mods)