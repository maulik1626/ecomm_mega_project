from django.urls import path
from carts.views import *


urlpatterns = [
    path("", cart, name="cart"),
]