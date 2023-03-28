from carts.models import Cart, CartItem
from carts.views import _cart_id


# Context processor goes here
def cart_counter(request):

    cart_items_len = 0
    
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart)
            for cart_item in cart_items:
                cart_items_len += cart_item.quantity
        except Cart.DoesNotExist:
            cart_items_len = 0
    
    return dict(cart_items_len=cart_items_len)
    

