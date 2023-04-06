from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages as msgs
from store.views import store
from wishlists.views import add_to_wishlist, wishlist as wishlist_view
from wishlists.models import WishlistItem
from django.http import JsonResponse


# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    """Add a quantity of the specified product to the cart."""
    product = Variation.objects.get(id=product_id)
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))    # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)        # check if the product is already in the cart using the product_id and cart_id 
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(        # if the product is not in the cart, then create a new cart_item
            product=product,                # and add the product to the cart
            cart=cart,                      # and set the cart_id to the cart_id present in the session
            quantity=1,                     # and set the quantity to 1
        )
    cart_item.save()
    
    product_name = cart_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    
    if cart_item.quantity > 1:
        msgs.info(request, f" {product_name} of size {cart_item.size} quantity is updated to {cart_item.quantity}.")
    else:
        msgs.info(request, f" {product_name} of size {cart_item.size}  is added to cart.")
    
    
    
    return redirect(store)

def soft_add_to_cart(request, product_id):
    """Add a quantity of the specified product to the cart."""
    print(f"\n\n\nTry in soft_add_to_cart\n\n\n")
    product = Variation.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))    # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, size=request.GET.get('size'))        # check if the product is already in the cart using the product_id and cart_id and size
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(        # if the product is not in the cart, then create a new cart_item
            product=product,                # and add the product to the cart
            cart=cart,                      # and set the cart_id to the cart_id present in the session
            quantity=1,                     # and set the quantity to 1
            size=request.GET.get('size'),                     # and set the quantity to inpuut quantity
        )
    cart_item.save()

    product_name = cart_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name

    if cart_item.quantity > 1:
        msgs.info(request, f" {product_name} of size {cart_item.size} quantity is updated to {cart_item.quantity}.")
    else:
        msgs.success(request, f" {product_name} of size {cart_item.size} is added to cart.")

    previous_url = request.META.get('HTTP_REFERER')
    request.session['previous_url'] = previous_url


    return redirect(previous_url)
    
    
def increase_in_cart(request, product_id, size):
    product = Variation.objects.get(id=product_id)
    
    wishlist_item = WishlistItem.objects.filter(product=product, wishlist__wishlist_id=_cart_id(request))
    wishlist_item.delete()
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))    # get the cart using the cart_id present in the session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()
    
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, size=size)        # check if the product is already in the cart using the product_id and cart_id 
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(        # if the product is not in the cart, then create a new cart_item
            product=product,                # and add the product to the cart
            cart=cart,                      # and set the cart_id to the cart_id present in the session
            size=size,
            quantity=1,                     # and set the quantity to 1
        )
    cart_item.save()
    
    product_name = cart_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    
    if cart_item.quantity > 1:
        msgs.info(request, f" {product_name}'s quantity is updated to {cart_item.quantity}.")
    else:
        msgs.info(request, f" {product_name} is added to cart.")
    
    
    
    return redirect("cart")
    

def cart(request, total=0, quantity=0, cart_items=None):
    context = {}
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.discount_price:
                total += (cart_item.product.discount_price * cart_item.quantity)
            else:
                total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (18 * total) / 100
        grand_total = total + tax
        tax = round(tax, 2)
        grand_total = round(grand_total, 2)
        context = {
            "total": total,
            "quantity": quantity,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
        }   
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    
    
    if cart_items.count() == 0:
        cart_empty_message = "Your cart is empty."
        context.update(
            {
                "cart_empty": True, 
                "cart_empty_message": cart_empty_message,
            }
        )
    
    return render(request, "carts/cart.html", context=context) 

def reduce_from_cart(request, product_id, size):
    """Reduce the quantity of the specified product to the cart."""
    product = Variation.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, size=size)
    product_name = cart_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        msgs.info(request, f" {product_name}'s quantity is updated to {cart_item.quantity}.")
    else:
        cart_item.delete()
        msgs.warning(request, f" {product_name} removed from cart.")
    cart.save()
    return redirect('cart')

def delete_from_cart(request, product_id, size):
    """Delete the specified product from the cart."""    
    product = Variation.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart, size=size)
    cart_item.delete()
    cart.save()
    
    product_name = cart_item.product.product_name
    product_name = product_name[:20] + "..." if len(product_name) > 20 else product_name
    
    msgs.warning(request, f" {product_name} removed from cart.")
    
    return redirect('cart')

def cart_to_wishlist(request, product_id, size):
    """Move the specified product from the cart to the wishlist."""
    
    
    # removing from cart
    delete_from_cart(request, product_id, size)
    
    # adding to wishlist
    add_to_wishlist(request, product_id)
    
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    if cart_items.count() == 0:
        return redirect(wishlist_view)
    
    
    return redirect('cart')

# TODO: make a function that notifies the user that the product is out of stock but in the cart

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    context = {}
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            if cart_item.product.discount_price:
                total += (cart_item.product.discount_price * cart_item.quantity)
            else:
                total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (18 * total) / 100
        grand_total = total + tax
        tax = round(tax, 2)
        grand_total = round(grand_total, 2)
        
        context = {
            "total": total,
            "quantity": quantity,
            "cart_items": cart_items,
            "tax": tax,
            "grand_total": grand_total,
        }   
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    
    
    
    if cart_items.count() == 0:
        cart_empty_message = "Your cart is empty."
        context.update(
            {
                "cart_empty": True, 
                "cart_empty_message": cart_empty_message,
            }
        )
    
    return render(request, "carts/checkout.html", context=context)