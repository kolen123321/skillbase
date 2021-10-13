from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_token
from .models import SecretCode
from .backends import authenticate
import datetime

from django.http import HttpResponseRedirect

import time


class AuthRedirectView(APIView):

    def get(self, request):
        auth_code = request.GET['auth_code']
        request.session['auth_code'] = auth_code
        return HttpResponseRedirect(f"https://discord.com/api/oauth2/authorize?client_id=895371122655244328&redirect_uri=http%3A%2F%2F{request.META['HTTP_HOST']}%2Fapi%2Fv1%2Fauth%2Flogin%2F&response_type=code&scope=identify")

class AuthView(APIView):

    def get(self, request):
        request_uri = f"http://{request.META['HTTP_HOST']}/api/v1/auth/login/"
        code = request.GET['code']
        token = get_token(code, request_uri)
        user = authenticate(token)
        for i in SecretCode.objects.filter(expire__lt=datetime.datetime.now()):
            i.delete()
        if not SecretCode.objects.filter(code=request.session['auth_code']).exists():
            secret = SecretCode()
            secret.user = user
            secret.code = request.session['auth_code']
            secret.save()
        del request.session['auth_code']
        return render(request, 'success.html')

class GetJWTView(APIView):

    def get(self, request):
        code = request.GET['auth_code']
        if not SecretCode.objects.filter(code=code).exists():
            return Response({
                'success': False,
                'message': 'Code not found.'
            }, status=404)
        if SecretCode.objects.get(code=code).expire.timestamp() < datetime.datetime.now().timestamp():
            SecretCode.objects.get(code=code).delete()
            return Response({
                'success': False,
                'message': 'Code expired.'
            }, status=400)
        code = SecretCode.objects.get(code=code)
        user = code.user
        code.delete()
        for i in SecretCode.objects.filter(expire__lt=datetime.datetime.now()):
            i.delete()
        return Response({
            'token': user.token(request)
        })