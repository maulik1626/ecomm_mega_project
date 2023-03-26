from django.urls import path
from wishlists.views import *

urlpatterns = [
    path("", wishlist, name="wishlist"),
    path("?add_to_wishlist=?/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("?cart_to_wishlist=?/<int:product_id>/", cart_to_wishlist, name="cart_to_wishlist"),
    path("?remove_from_wishlist=?/<int:product_id>/", remove_from_wishlist, name="remove_from_wishlist")
]