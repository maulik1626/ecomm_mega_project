from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from carts.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages as msgs
from store.views import store
from wishlists.models import WishlistItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    """Add a quantity of the specified product to the cart."""
    product = Product.objects.get(id=product_id)
    
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
        cart_item = CartItem.objects.get(product=product, cart=cart)        # check if the product is already in the cart using the product_id and cart_id 
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(        # if the product is not in the cart, then create a new cart_item
            product=product,                # and add the product to the cart
            cart=cart,                      # and set the cart_id to the cart_id present in the session
            quantity=1,                     # and set the quantity to 1
        )
    cart_item.save()
    
    if cart_item.quantity > 1:
        msgs.info(request, f"The quantity is updated to {cart_item.quantity}.")
    else:
        msgs.info(request, "The product added to cart.")
    
    
    
    return redirect(store)

def increase_in_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    
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
        cart_item = CartItem.objects.get(product=product, cart=cart)        # check if the product is already in the cart using the product_id and cart_id 
        cart_item.quantity += 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(        # if the product is not in the cart, then create a new cart_item
            product=product,                # and add the product to the cart
            cart=cart,                      # and set the cart_id to the cart_id present in the session
            quantity=1,                     # and set the quantity to 1
        )
    cart_item.save()
    
    if cart_item.quantity > 1:
        msgs.info(request, f"The quantity is updated to {cart_item.quantity}.")
    else:
        msgs.info(request, "The product added to cart.")
    
    
    
    return redirect("cart")
    

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (18 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    
    if cart_items.count() == 0:
        cart_empty_message = "Your cart is empty."
        context.update(
            {
                "cart_empty": True, 
                "cart_empty_message": cart_empty_message,
            }
        )
    
    return render(request, "carts/cart.html", context=context) 

def reduce_from_cart(request, product_id):
    """Reduce the quantity of the specified product to the cart."""
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    cart.save()
    
    msgs.info(request, f"The quantity is updated to {cart_item.quantity}.")
    
    return redirect('cart')

def delete_from_cart(request, product_id):
    """Delete the specified product from the cart."""    
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    cart.save()
    
    msgs.warning(request, "Product(s) removed from cart.")
    
    return redirect('cart')