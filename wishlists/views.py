from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as msgs
from wishlists.models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from store.views import store

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
    
    if wishlist_items.count == 0:
        msgs.info(request, "Your wishlist is empty.")
        
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
        msgs.info(request, "Product already in wishlist.")
        item_in_wishlist = True
    except WishlistItem.DoesNotExist:
        wishlist_item = WishlistItem.objects.create(
            product=product,
            wishlist=wishlist,
        )
        wishlist_item.save()
        msgs.success(request, "Product added to wishlist.")
    
    wishlist_item.save()
    return redirect(store)

def remove_from_wishlist(request, product_id):
    wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product, wishlist=wishlist)
    wishlist_item.delete()
    wishlist.save()
    msgs.warning(request, "Product removed from wishlist.")
    return redirect("wishlist")