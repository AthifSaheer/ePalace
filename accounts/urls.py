from . import views
from django.urls import path


urlpatterns = [
    # User
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),

    # Admin
    path('admin-login', views.admin_login, name='admin_login'),
    path('adminlogout', views.admin_logout, name='admin_logout'),
]