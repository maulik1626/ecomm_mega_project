from carts.models import Cart, CartItem
from carts.views import _cart_id


# Context processor goes here
def cart_counter(request):

    cart_items_len = 0
    
    if 'admin' in request.path:
        return {}
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        print(f"\n\n\ncart: {cart}\n\n\n")
        cart_items = CartItem.objects.all().filter(cart=cart)
        print(f"\n\n\ncart_items: {cart_items}\n\n\n")
        for cart_item in cart_items:
            cart_items_len += cart_item.quantity
    
    return dict(cart_items_len=cart_items_len)
    

