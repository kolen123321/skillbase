from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import SecretCode
from mods.models import HaveMod, Mod

from accounts.backends import JWTGetModAuthentication

class ModsView(APIView):

    authentication_classes = [JWTGetModAuthentication]

    def get(self, request):
        mod = request.GET['mod']
        user = request.user
        if not Mod.objects.filter(name=mod).exists():
            return Response({
                'success': False,
                'message': 'Mod not found.'
            }, status=404)
        mod = Mod.objects.get(name=mod)
        if not mod in HaveMod.objects.get(user=user).mods.all():
            return Response({
                'success': False,
                'message': 'You don\'t have this mod.'
            })
        file = open(mod.code, "rb+").read()
        response = HttpResponse(file, content_type="application/class")
        response['Content-Disposition'] = f'filename="{mod.name}.class"'
        return response