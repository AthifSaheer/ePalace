from django.shortcuts import render
from .models import Product

def home(request):
    product = Product.objects.all().order_by('-id')
    return render(request, 'User/index.html' ,{'product':product})


def product_detail(request, slug):
    url_slug = slug
    product_detailed = Product.objects.filter(slug=url_slug)
    return render(request, 'User/productdetails.html' ,{'product_detailed':product_detailed})

