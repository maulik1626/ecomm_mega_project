from django.db import models
from store.models import Product

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "CartItem"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    # def img_preview(self):
    #     return self.product.image.url.split("/")[-1]
    
    def __str__(self):
        return self.product.product_name
    