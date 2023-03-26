from django.shortcuts import render
from random import shuffle
from store.models import Product
from category.models import Category
from wishlists.models import Wishlist, WishlistItem


# Create your views here.

# STEP 1: Make a home view function and render home.html
# STEP 2: Make a templates folder in the project root and go to settings.py file to register that folder

# STEP 48: show the products in the home page
def home(request):
    # documentaion: https://docs.djangoproject.com/en/3.2/ref/models/querysets/
    products = Product.objects.filter(is_available=True).order_by("-created_date")
    print(products)
    
    categories = Category.objects.all()
    
    products = list(products)
    shuffle(products)
    
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    
    wishlist = Wishlist.objects.get(wishlist_id=wishlist)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)    
    wishlist_items = [wishlist_item.product.product_name for wishlist_item in wishlist_items]
    
    context = {
        "products": products[:7], 
        "categories": categories,
        "title": "Home",
        "wishlist_items" : wishlist_items,
    }
    return render(request, "home.html", context=context)

# STEP 49: go to templates/home.html and show the products in the home page
# STEP 50: go to ecomm_project/urls.py and add the store url