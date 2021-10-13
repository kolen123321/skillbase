from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.AuthView.as_view()),
    path('', views.AuthRedirectView.as_view()),
    path('get/', views.GetJWTView.as_view()),
]
