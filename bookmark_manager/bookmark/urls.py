from django.contrib import admin
from django.urls import path, include

from . import views

#Urls patterns for /api
urlpatterns = [
    path('create', views.create),
    path('browse', views.browse),
]