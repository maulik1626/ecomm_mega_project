from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import Category

# Create your views here.

# STEP 53: make a store function to render the store page and bring in all the products to the store page
# STEP 54: go to store/templates/store/store.html and make the store page
# STEP 55: go to store/urls.py file and give categories url using slug
# STEP 56: make a context_processor for the categories to be available accross project. Make a file named category/context_processors.py
def store(request, category_slug=None):
    """This function is used to show the products in the store page. If the category slug is not None, then it will show the products of that category. If the category slug is None, then it will show all the products. It will also show the categories in the store page. It will also show the number of products in the store page."""
    categories = None
    products = None
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        categories = Category.objects.all()
        product_count = products.count()
    
    

    context = {
        "products": products,
        "categories": categories,
        "product_count": product_count,
        "title": "Store",
    }
    
    return render(request, "store/store.html", context=context)

# STEP 62: make a product_detail function to render the product_detail page and bring in all the product details to the product_detail page
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
    except Exception as e:
        raise e
    context = {
        "single_product" : single_product,
    }
    return render(request, "store/product_detail.html", context=context)