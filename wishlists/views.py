from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msgs
from wishlists.models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.views import store
# from carts.views import add_to_cart

# Create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist

def wishlist(request, wishlist_items=None):
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)
    except ObjectDoesNotExist:
        pass
    context = {
        "wishlist_items": wishlist_items,
    }
    
    if wishlist_items.count() == 0:
        wishlist_empty_message = "Your wishlist is empty"
        context["wishlist_empty"] = True 
        context["wishlist_empty_message"] = wishlist_empty_message
    
    context["title"] = "Wishlist"

        
    return render(request, "wishlists/wishlist.html", context=context)

def add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(
            wishlist_id=_wishlist_id(request)
        )
    wishlist.save()
    
    try:
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
        product_name = wishlist_item.product.product_name
        product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    
        msgs.info(request, f" {product_name} already in wishlist.")
    except WishlistItem.DoesNotExist:
        wishlist_item = WishlistItem.objects.create(
            product=product,
            wishlist=wishlist,
        )
        wishlist_item.save()
        product_name = wishlist_item.product.product_name
        product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    
        msgs.success(request, f" {product_name} is added to wishlist.")
    
    wishlist_item.save()
    return redirect(store)

def remove_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    wishlist.save()
    product_name = wishlist_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    msgs.warning(request, f" {product_name} removed from wishlist.")
    return redirect("wishlist")

# TODO: Implement wishlist to cart
# def wishlist_to_cart(request, product_id):
#     """Move a product from the wishlist to the cart."""
    # removing from wishlist
    # remove_from_wishlist(request, product_id)
    # adding to cart
    # add_to_cart(request, product_id)

    # wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    # wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active=True)

    # if wishlist_items.count() == 0:
    #     return redirect(cart)
    
    return redirect('wishlist')

def soft_remove_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    wishlist.save()

    # Store the previous URL in the session
    previous_url = request.META.get('HTTP_REFERER')
    request.session['previous_url'] = previous_url
    
    product_name = wishlist_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    msgs.warning(request, f" {product_name} removed from wishlist.")
    
    # Redirect the user to the wishlist page
    return redirect(previous_url)

def soft_add_to_wishlist(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(
            wishlist_id=_wishlist_id(request)
        )
    wishlist.save()

    try:
        wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    except WishlistItem.DoesNotExist:
        wishlist_item = WishlistItem.objects.create(
            product=product,
            wishlist=wishlist,
        )
        wishlist_item.save()
    
    wishlist_item.save()
    
    # Store the previous URL in the session
    previous_url = request.META.get('HTTP_REFERER')
    request.session['previous_url'] = previous_url
    
    # Redirect the user to the wishlist page
    return redirect(previous_url)

# TODO: make a function that notifies the user that the product is out of stock but in the wishlist