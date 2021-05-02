from django.contrib import admin
from .models import Category, SubCategory, Product

admin.site.register([Category, SubCategory, Product])