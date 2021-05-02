from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='home'),
    path('products/<slug:slug>/', views.hai, name="prd_detail"),
]