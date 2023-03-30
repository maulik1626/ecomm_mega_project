from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from store.models import Product, Variation, ProductColor
from category.models import Category
from wishlists.models import Wishlist, WishlistItem
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from carts.models import Cart, CartItem

# Create your views here.

# STEP 53: make a store function to render the store page and bring in all the products to the store page
# STEP 54: go to store/templates/store/store.html and make the store page
# STEP 55: go to store/urls.py file and give categories url using slug
# STEP 56: make a context_processor for the categories to be available accross project. Make a file named category/context_processors.py


def _sort_sizes(sizes: list) -> list:
    """This function is used to sort the sizes. It will sort the sizes in the order of XS, S, M, L, XL, XXL."""
    try:
        return sorted(sizes, key=lambda x: ['XXXS', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL'].index(x))
    except:
        return sorted([int(i) for i in sizes])


def store(request, category_slug=None):
    """This function is used to show the products in the store page. If the category slug is not None, then it will show the products of that category. If the category slug is None, then it will show all the products. It will also show the categories in the store page. It will also show the number of products in the store page."""
    categories = None
    products = None
    items_per_page = 6
    # TODO: Add pagination to the store page
    # TODO: Add search functionality to the store page
    # TODO: Add sorting functionality to the store page
    # TODO: Add filtering functionality to the store page
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        all_products = Variation.objects.filter(product__category=categories, is_available=True)
    else:
        all_products = Variation.objects.all().filter(is_available=True)
        # variations = Variation.objects.all().filter(is_available=True)

    products = _product_by_color(all_products)
    
    all_products_count = len(products)
    
    paginator = Paginator(products, items_per_page)
    page = request.GET.get('page')
    page_items = paginator.get_page(page) 
    
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    
    wishlist = Wishlist.objects.get(wishlist_id=wishlist)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)
    wishlist_items = [wishlist_item.product.product_name for wishlist_item in wishlist_items]
    
    
    context = {
        "title": "Store",
        'products' : page_items,
        "wishlist_items": wishlist_items,
        "product_count": all_products_count,
    }
    
    return render(request, "store/store.html", context=context)

def _product_by_color(all_products):
    products = []
    check_list = []
    for i in all_products:
        product = f"{i.product.product_name} {i.color}"
        if product in check_list:
            pass
        else:
            products.append(i)
            check_list.append(product)
    return products

# STEP 62: make a product_detail function to render the product_detail page and bring in all the product details to the product_detail page
def product_detail(request, category_slug, product_slug, color_id):
    cart_item = None
    wishlist_item = None
    try:
        products = Variation.objects.filter(product__category__slug = category_slug, product__slug = product_slug, color_id = color_id, is_available=True).first()
        # TODO: if the product is in the cart, show the add to cart button as Add one more, quantity as cartitem_quantity and disable the quantity input, and show the remove from cart button
        
        # Get a list of unique sizes from the products with the same name
        variations = Variation.objects.filter(product__category__slug = category_slug, product__slug = product_slug, color_id = color_id, is_available=True)
        
        print("\n\n\nI am here")
        print(f"\n\n\n{products}\n\n\n")
        print(f"\n\n\n{variations}\n\n\n")
        
        # tags = single_product.tags.values_list('name', flat=True).order_by('-name')
        # print(f"\n\n\n{tags}\n\n\n")

        session_id = request.session.session_key
        if not session_id:
            session_id = request.session.create()
        
        try:
            cart = Cart.objects.get(cart_id=session_id)
        except Cart.DoesNotExist:
            pass
        
        try:
            cart_item = CartItem.objects.filter(product=products, cart=cart)        
        except CartItem.DoesNotExist:
            pass
        
        try:
            wishlist = Wishlist.objects.get(wishlist_id=session_id)
        except Wishlist.DoesNotExist:
            pass
        
        try:
            wishlist_item = WishlistItem.objects.get(product=products, wishlist=wishlist)        
        except WishlistItem.DoesNotExist:
            pass

        
        # TODO: if the product is in the wishlist, show the add to wishlist button as remove from wishlist button
        # TODO: Display related products in the product detail page
    except Exception as e:
        raise e
    
    product_colors = [i.color for i in variations]
    
    print(f"\n\n\n{product_colors}\n\n\n")
    # print(f"\n\n\n{sizes}\n\n\n")
    
    # get the list of sizes using values_list
    try:
        sizes = [int(i.size) for i in variations]
    except:
        sizes = [str(i.size) for i in variations]
        
    sorted_sizes = _sort_sizes(sizes)
    
    print("sortedSizes")
    print(f"{products}")
    print(f"\n\n\n{sorted_sizes}\n\n\n")
    
    unique_colors = list(set(product_colors))
    
    context = {
        "title": "Product Detail",
        "single_product" : products,
        "cart_item" : cart_item,
        "wishlist_item" : wishlist_item,
        "sizes" : sorted_sizes,
        # "tags" : tags,
        "product_colors" : unique_colors,
        "variations" : variations,

    }
    return render(request, "store/product_detail.html", context=context)

#TODO: make a function that notify the user if the product is back in stock if the user has subscribed to the product's in stock notification

def search(request):
    context = {}
    product_not_found = None
    if 'keyword' in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            
            all_products = Variation.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(product__category__category_name__icontains=keyword) | Q(product__product_name__icontains=keyword) | Q(color__color_name__icontains=keyword)
                , is_available=True
            )

            products = _product_by_color(all_products)
            
            print(f"\n\n\n{products}\n\n\n")
            
            product_count = len(products)

            if product_count < 1:
                product_not_found = True
                context["product_not_found"] = product_not_found
            
        else:
            all_products = Variation.objects.order_by('-created_date').filter(is_available=True)
            
            products = _product_by_color(all_products)
            
            product_count = len(products)

    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    
    wishlist = Wishlist.objects.get(wishlist_id=wishlist)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)    
    wishlist_items = [wishlist_item.product.product_name for wishlist_item in wishlist_items]

    
    context["products"] = products
    context["product_count"] = product_count
    context["wishlist_items"] = wishlist_items
    context["keyword"] = keyword
    
    print(context)
    
    return render(request, "store/store.html", context=context)



