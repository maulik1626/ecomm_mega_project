from django.contrib import admin
from carts.models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')
    readonly_fields = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'cart', 'size', 'quantity', 'is_active')
    readonly_fields = ('product', 'user', 'cart', 'size', 'quantity', 'is_active')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)