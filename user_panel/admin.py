from django.contrib import admin
from .models import *

admin.site.register([Category, SubCategory, Product, Cart, ProfileImage, CartItem])