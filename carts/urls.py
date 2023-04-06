from django.urls import path
from carts.views import *


urlpatterns = [
    path("", cart, name="cart"),
    path("add_to_cart/<int:product_id>", add_to_cart, name="add_to_cart"),
    path("soft_add_to_cart/<int:product_id>", soft_add_to_cart, name="soft_add_to_cart"),
    path('increase/<int:product_id>/<str:size>/', increase_in_cart, name="increase_in_cart"),
    path('reduce/<int:product_id>/<str:size>/', reduce_from_cart, name='reduce_from_cart'),
    path("delete/<int:product_id>/<str:size>/", delete_from_cart, name="delete_from_cart"),
    path("cart_to_wishlist/<int:product_id>", cart_to_wishlist, name="cart_to_wishlist"),
    path("cart_to_wishlist/<int:product_id>/<str:size>/", cart_to_wishlist, name="cart_to_wishlist"),
    path('checkout/', checkout, name='checkout'),
]