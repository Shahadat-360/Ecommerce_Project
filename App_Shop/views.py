from django.shortcuts import render
# view import
from django.views.generic import ListView, DetailView

from App_Shop.models import Product, Category


# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'
