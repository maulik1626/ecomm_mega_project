from django.contrib import admin
from wishlists.models import Wishlist, WishlistItem

# Register your models here.
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('wishlist_id', 'date_added')
    readonly_fields = ('wishlist_id', 'date_added')

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('brand', 'product', 'wishlist', 'is_active')
    readonly_fields = ('brand', 'product', 'wishlist', 'is_active')
    
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)