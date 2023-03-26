from django.urls import path
from carts.views import *


urlpatterns = [
    path("", cart, name="cart"),
    path("add_to_cart/<int:product_id>", add_to_cart, name="add_to_cart"),
    path("increase_in_cart/<int:product_id>", increase_in_cart, name="increase_in_cart"),
    path("reduce_from_cart/<int:product_id>", reduce_from_cart, name="reduce_from_cart"),
    path("delete_from_cart/<int:product_id>", delete_from_cart, name="delete_from_cart"),
    path("cart_to_wishlist/<int:product_id>", cart_to_wishlist, name="cart_to_wishlist"),
]