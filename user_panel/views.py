from django.shortcuts import render
from .models import Product

def home(request):
    product = Product.objects.all()
    return render(request, 'User/index.html',{'product':product})


def hai(request):
    return render(request, 'productdetails.html')