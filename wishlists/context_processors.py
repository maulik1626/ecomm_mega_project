from wishlists.models import Wishlist, WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from wishlists.views import _wishlist_id

# Context processor goes here
def wishlist_counter(request):
    
    if 'admin' in request.path:
        return {}
    else:
        wishlist = Wishlist.objects.filter(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.all().filter(wishlist=wishlist[:1])

    
    return dict(wishlist_items_len=wishlist_items.count())
    
            
            
