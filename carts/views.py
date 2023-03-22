from django.shortcuts import render, redirect
from store.models import Product
from carts.models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
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
    return redirect('cart')

def cart(request):
    return render(request, "carts/cart.html")