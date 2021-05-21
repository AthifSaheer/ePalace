from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    # User
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

    path('send_mail/', views.send_mail ,name='send_mail'),

    path('change_password/request/email/', views.change_password_request_email ,name='change_password_request_email'),
    path('change_password/<int:id>/', views.change_password ,name='change_password'),
    
    path('login/with_otp', views.login_with_otp, name='login_with_otp'),
    path('login/with_otp/enter_otp/<int:otp>/<str:username>/', views.enter_otp, name='enter_otp'),

    # Admin
    path('admin-login/', views.admin_login, name='admin_login'),
    path('adminlogout/', views.admin_logout, name='admin_logout'),


    path('ref-link/', views.ref_link, name='ref_link'),
    path('signup/ref/link/<str:ref_code>/', views.signup_with_ref_code, name='signup_with_ref_code'),
]
