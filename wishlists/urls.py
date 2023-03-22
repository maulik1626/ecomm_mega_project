from django.urls import path
from wishlists.views import *

urlpatterns = [
    path("", wishlist, name="wishlist"),
]