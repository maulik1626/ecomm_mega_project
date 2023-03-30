from django.urls import path
from store.views import *

# STEP 52: add the store url to the urlpatterns list and make its view function in store/views.py
# STEP 61: add the product_detail url to the urlpatterns list and make its view function in store/views.py
urlpatterns = [
    path("", store, name="store"),
    path("category/<slug:category_slug>/", store, name="products_by_category"),
    path("category/<slug:category_slug>/<slug:product_slug>/<int:color_id>/", product_detail, name="product_detail"),
    path("search/", search, name="search"),
]