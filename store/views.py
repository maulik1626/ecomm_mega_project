from django.shortcuts import render, get_object_or_404
from store.models import Product
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
def store(request, category_slug=None):
    """This function is used to show the products in the store page. If the category slug is not None, then it will show the products of that category. If the category slug is None, then it will show all the products. It will also show the categories in the store page. It will also show the number of products in the store page."""
    categories = None
    products = None
    items_per_page=3
    
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        product_count = products.count()
        
        paginator = Paginator(products, items_per_page)
        page = request.GET.get('page')
        page_items = paginator.get_page(page) 
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        categories = Category.objects.all()
        product_count = products.count()
        
        
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
        "products": page_items,
        "categories": categories,
        "product_count": product_count,
        "title": "Store",
        "wishlist_items" : wishlist_items,
    }
    
    return render(request, "store/store.html", context=context)

# STEP 62: make a product_detail function to render the product_detail page and bring in all the product details to the product_detail page
def product_detail(request, category_slug, product_slug):
    cart_item = None
    wishlist_item = None
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        # TODO: if the product is in the cart, show the add to cart button as Add one more, quantity as cartitem_quantity and disable the quantity input, and show the remove from cart button
        
        sizes = single_product.size.values_list('name', flat=True).order_by('-name') # get the list of sizes
        try:
            sizes = [int(size) for size in sizes if size != ''] # remove the empty string from the sizes list
            sizes.sort() # sort the sizes list
            sizes = [str(size) for size in sizes] # convert the sizes list to string
        except:
            sizes = [size for size in sizes if size != ''] # remove the empty string from the sizes list
        
        tags = single_product.tags.values_list('name', flat=True).order_by('-name')

        session_id = request.session.session_key
        if not session_id:
            session_id = request.session.create()
        
        try:
            cart = Cart.objects.get(cart_id=session_id)
        except Cart.DoesNotExist:
            pass
        
        try:
            cart_item = CartItem.objects.get(product=single_product, cart=cart, size=single_product.size)        
        except CartItem.DoesNotExist:
            pass
        
        try:
            wishlist = Wishlist.objects.get(wishlist_id=session_id)
        except Wishlist.DoesNotExist:
            pass
        
        try:
            wishlist_item = WishlistItem.objects.get(product=single_product, wishlist=wishlist)        
        except WishlistItem.DoesNotExist:
            pass

        
        # TODO: if the product is in the wishlist, show the add to wishlist button as remove from wishlist button
        # TODO: Display related products in the product detail page
    except Exception as e:
        raise e
    
    product_color = str(single_product.color)
    product_color = [i for i in product_color if i.isalpha()]
    product_color = ''.join(product_color)
    
    context = {
        "single_product" : single_product,
        "cart_item" : cart_item,
        "wishlist_item" : wishlist_item,
        "sizes" : sizes,
        "tags" : tags,
        "product_color" : product_color,
    }
    return render(request, "store/product_detail.html", context=context)

#TODO: make a function that notify the user if the product is back in stock if the user has subscribed to the product's in stock notification

def search(request):
    context = {}
    product_not_found = None
    if 'keyword' in request.GET:
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword) | Q(category__category_name__icontains=keyword)
            )
            product_count = products.count()

            if product_count < 1:
                product_not_found = True
                context["product_not_found"] = product_not_found
            
            no_keyword = True
        else:
            products = Product.objects.order_by('-created_date').filter(is_available=True)
            no_keyword = False
            product_count = products.count()
        wishlist = request.session.session_key


    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    
    wishlist = Wishlist.objects.get(wishlist_id=wishlist)
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)    
    wishlist_items = [wishlist_item.product.product_name for wishlist_item in wishlist_items]

    
    context["products"] = products
    context["product_count"] = product_count
    context["wishlist_items"] = wishlist_items
    
    print(context)
    
    return render(request, "store/store.html", context=context)