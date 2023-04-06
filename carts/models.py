from django.db import models
from accounts.models import Account
from store.models import Variation

# Create your models here.
class Cart(models.Model):
    """This model is used to store the cart id and the date when the cart is created."""
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = "Cart"
        ordering = ["date_added"]
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
    
    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    """This model is used to store the product, cart, quantity and the status of the cart item."""
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "CartItem"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        
    
    def sub_total(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        else:
            return self.product.price * self.quantity
    
    # def img_preview(self):
    #     return self.product.image.url.split("/")[-1]
    
    def __str__(self):
        return self.product.product_name
    