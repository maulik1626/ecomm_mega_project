from django.shortcuts import render
from random import shuffle
from store.models import Product, Variation
from category.models import Category
from wishlists.models import Wishlist, WishlistItem


# Create your views here.

# STEP 1: Make a home view function and render home.html
# STEP 2: Make a templates folder in the project root and go to settings.py file to register that folder

# STEP 48: show the products in the home page
def home(request):
    # documentaion: https://docs.djangoproject.com/en/3.2/ref/models/querysets/
    all_products = Variation.objects.all().filter(is_available=True)

    products = []
    check_list = []
    for i in all_products:
        product = f"{i.product.product_name} {i.color}"
        if product in check_list:
            pass
        else:
            products.append(i)
            check_list.append(product)
    
    print(products)
    
    categories = Category.objects.all()
    
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    
    try:
        wishlist = Wishlist.objects.get(wishlist_id=wishlist)
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)    
        wishlist_items = [wishlist_item.product.product_name for wishlist_item in wishlist_items]
    except Wishlist.DoesNotExist:
        wishlist_items = []
        
    
    context = {
        "products": products[:7], 
        "categories": categories,
        "title": "Home",
        "wishlist_items" : wishlist_items,
    }
    return render(request, "home.html", context=context)

# STEP 49: go to templates/home.html and show the products in the home page
# STEP 50: go to ecomm_project/urls.py and add the store url