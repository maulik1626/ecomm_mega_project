from django.db import models
from category.models import Category
from django.utils.html import mark_safe
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    """This class is used to create the product model"""
    product_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        """This class is used to set the default ordering of the products"""
        ordering = ['-created_date']
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.product_name
    
    def img_preview(self):
        """This function is used to show the image preview in the admin panel"""
        return mark_safe(f'<img src="{self.images.url}" width="50" />')
    
    # STEP 63: add the get_url function to the product model
    def get_url(self):
        """This function is used to get the absolute url of the product"""
        return reverse("product_detail", args=[self.category.slug, self.slug])

    # STEP 44: register the product model in the admin.py file of the store