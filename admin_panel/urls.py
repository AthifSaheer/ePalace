from . import views
from django.urls import path


urlpatterns = [
    # Admin home page
    path('', views.admin_home, name='admin_home'),

    # Product management
    path('products', views.products, name='products'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('create_products', views.create_products, name='create_products'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    
    # User management
    path('users', views.users, name='users'),
    path('block_user/<int:id>', views.block_user, name='block_user'),
    path('un_block_user/<int:id>', views.un_block_user, name='un_block_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    
    # Category management
    path('categories', views.categories, name='categories'),
    path('create_category', views.create_category, name='create_category'),
    path('create_sub_category', views.create_sub_category, name='create_sub_category'),

    # Order management
    # path('orders', views.orders, name='orders'),

]