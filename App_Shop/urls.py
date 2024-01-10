from django.urls import path
from django.shortcuts import redirect, render, reverse
from App_Shop import views

app_name = 'App_Shop'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
]
