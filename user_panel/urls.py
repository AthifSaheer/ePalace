from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='user_home'),
    path('products/<slug:slug>/', views.product_detail, name="prd_detail"),

    path('add-to-cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('cart', views.cart, name="cart"),
    path('item_decrement/<int:id>', views.item_decrement, name="item_decrement"),
    path('remove_item/<int:id>', views.remove_item, name="remove_item"),
    
    path('check_out/', views.check_out, name="check_out"),
    path('order_placed', views.order_place_animation, name="order_place_animation"),

    path('order', views.order, name="order"),
    path('order-detail/<int:id>', views.order_detail, name="order_detail"),
    
    path('profile/<int:id>', views.profile, name="profile"),
    path('change_profile_image/<int:id>', views.change_profile_image, name="change_profile_image"),
]