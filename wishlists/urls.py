from django.urls import path
from wishlists.views import *

urlpatterns = [
    path("", wishlist, name="wishlist"),
    path("add_to_wishlist/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("remove_from_wishlist/<int:product_id>/", remove_from_wishlist, name="remove_from_wishlist"),
    # path("wishlist_to_cart/<int:product_id>/", wishlist_to_cart, name="wishlist_to_cart"),
]
