from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='user_home'),
    path('products/<slug:slug>/', views.product_detail, name="prd_detail"),
]