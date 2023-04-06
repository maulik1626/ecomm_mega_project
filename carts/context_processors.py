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
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart)
            for cart_item in cart_items:
                cart_items_len += cart_item.quantity
        except Cart.DoesNotExist:
            print(f"\n\n\nIn Except Block now\n\n\n")
            cart_items_len = 0
    
    return dict(cart_items_len=cart_items_len)
    

