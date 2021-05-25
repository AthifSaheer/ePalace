from django.urls import path
from . import views
# from django.conf.urls import url


urlpatterns = [
    # HOME AND PRODUCT LISTING ------------------------------------------
    path('', views.home, name='user_home'),
    path('products/<slug:slug>/', views.product_detail, name="prd_detail"),
    path('category_wised_product/', views.category_wised_product, name="category_wised_product"),

    # SEARCH AND FILTER ------------------------------------------
    path('search/', views.search, name="search"),
    path('filter_data/', views.filter_data, name="filter_data"),

    # CART AND CHECKOUT ------------------------------------------
    path('add-to-cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('cart', views.cart, name="cart"),
    path('item_decrement/<int:id>', views.item_decrement, name="item_decrement"),
    path('remove_item/<int:id>', views.remove_item, name="remove_item"),
    
    path('check_out/', views.check_out, name="check_out"),
    path('order_placed/', views.order_place_animation, name="order_place_animation"),

    # ORDER ------------------------------------------
    path('order', views.order, name="order"),
    path('order-detail/<int:id>', views.order_detail, name="order_detail"),
    path('cancel_order/<int:id>', views.cancel_order, name="cancel_order"),
    
    # PAYMENTS ------------------------------------------
    path('profile/<int:id>', views.profile, name="profile"),
    path('change_profile_image/<int:id>', views.change_profile_image, name="change_profile_image"),
    path('add_address/<int:id>', views.add_address, name="add_address"),
    path('edit_address/<int:id>', views.edit_address, name="edit_address"),
    path('delete_address/<int:id>', views.delete_address, name="delete_address"),
    
    # PAYMENTS ------------------------------------------
    path('paypal/', views.paypal, name="paypal"),
    path('razorpay/', views.razorpay, name="razorpay"),

    # OFFER ------------------------------------------
    path('cupon/code/', views.cupon_code, name="cupon_code"),
]