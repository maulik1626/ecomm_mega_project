from django.db import models
from store.models import Product


class Wishlist(models.Model):
    wishlist_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = "Wishlist"
        ordering = ["date_added"]
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"
    
    def __str__(self) -> str:
        return self.wishlist_id

class WishlistItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "WishlistItem"
        verbose_name = "Wishlist Item"
        verbose_name_plural = "Wishlist Items"
    
    def __str__(self) -> str:
        return self.product.product_name
