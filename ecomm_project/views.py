from django.shortcuts import render
from random import shuffle
from store.models import Product
from category.models import Category

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
    
    context = {
        "products": products[:7], 
        "categories": categories,
    }
    return render(request, "home.html", context=context)

# STEP 49: go to templates/home.html and show the products in the home page
# STEP 50: go to ecomm_project/urls.py and add the store url