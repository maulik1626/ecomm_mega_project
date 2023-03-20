from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe

# Create your models here.

# STEP 22: Create a Category Model
class Category(models.Model):
    """This class is used to create a category model"""
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    # STEP 23: run pip install Pillow
    category_image = models.ImageField(upload_to="photos/categories/", blank=True)
    
    class Meta:
        """This class is used to give the plural name of the model"""
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.category_name

    def img_preview(self):
        """This function is used to show the image preview in the admin panel"""
        return mark_safe(f'<img src="{self.category_image.url}" width="50" />')
    
    # STEP 59: Make the get_url function here
    def get_url(self):
        """This function is used to get the absolute url of the category"""
        return reverse("products_by_category", args=[self.slug])
    
    
    # STEP 60: Move on to make a product detail url in store/urls.py

# STEP 24: Register to model and go to admin.py file


