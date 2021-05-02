from . import views
from django.urls import path


urlpatterns = [
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),

    path('admin-login', views.admin_login, name='admin_login'),
]