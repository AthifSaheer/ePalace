from . import views
from django.urls import path


urlpatterns = [
    # Admin home page
    path('', views.admin_home, name='admin_home'),
    path('monthly/sales-report', views.monthly_sales_report, name='monthly_sales_report'),
    path('yearly/sales-report', views.yearly_sales_report, name='yearly_sales_report'),
    path('convert/to/pdf', views.convert_to_pdf, name='convert_to_pdf'),

    # Product management
    path('products', views.products, name='products'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('create_products', views.create_products, name='create_products'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
    
    # User management
    path('users', views.users, name='users'),
    path('block_user/<str:username>', views.block_user, name='block_user'),
    path('un_block_user/<int:id>', views.un_block_user, name='un_block_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    
    # Category management
    path('categories', views.categories, name='categories'),

    path('create_category', views.create_category, name='create_category'),
    path('edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('delete/category/<int:id>', views.delete_category, name='delete_category'),

    path('create_sub_category', views.create_sub_category, name='create_sub_category'),
    path('edit_sub_category/<int:id>', views.edit_sub_category, name='edit_sub_category'),
    path('delete_sub_category/<int:id>', views.delete_sub_category, name='delete_sub_category'),

    # Order management
    path('orders', views.orders, name='orders'),
    path('orders/change/status/<int:id>', views.orders_status_change, name='orders_status_change'),

    # Offer management
    path('product/offer/', views.product_offer, name='product_offer'),
    path('create/product/offer/', views.create_product_offer, name='create_product_offer'),
    path('edit/product/offer/<int:id>/', views.edit_product_offer, name='edit_product_offer'),
    path('delete/product/offer/<int:id>/', views.delete_product_offer, name='delete_product_offer'),
    
    path('category/offer/', views.category_offer, name='category_offer'),
    path('create/category/offer/', views.create_category_offer, name='create_category_offer'),
    path('edit/category/offer/<int:id>/', views.edit_category_offer, name='edit_category_offer'),
    path('delete/category/offer/<int:id>/', views.delete_category_offer, name='delete_category_offer'),
    

    path('cupon/offer/', views.cupon_offer, name='cupon_offer'),
    path('create/cupon/offer/', views.create_cupon_offer, name='create_cupon_offer'),
    path('edit/cupon/offer/<int:id>/', views.edit_cupon_offer, name='edit_cupon_offer'),
    path('delete/cupon/offer/<int:id>/', views.delete_cupon_offer, name='delete_cupon_offer'),
]