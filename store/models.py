from django.db import models
from django.utils.text import slugify
from category.models import Category
from django.utils.html import mark_safe
from django.urls import reverse

# Create your models here.
class ProductBrand(models.Model):
    """This class is used to create the product brand model"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Brand'
        verbose_name_plural = 'Product Brands'

class ProductType(models.Model):
    """This class is used to create the product type model"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

class ProductTags(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Tag'
        verbose_name_plural = 'Product Tags'
        
class ProductColor(models.Model):
    """This class is used to create the product color model"""
    color_name = models.CharField(max_length=200, unique=True)
    color_hex = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    

    def __str__(self):
        return self.color_name
    
    class Meta:
        verbose_name = 'Product Color'
        verbose_name_plural = 'Product Colors'

class ProductVariationCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Variation Category'
        verbose_name_plural = 'Product Variation Categories'

class ProductSize(models.Model):
    name = models.CharField(max_length=200, unique=True)
    product_variation_category = models.ForeignKey(ProductVariationCategory, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Size'
        verbose_name_plural = 'Product Sizes'

class Variation(models.Model):
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True)
    variation_category = models.ForeignKey(ProductVariationCategory, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.variation_value
    
    def img_preview(self):
        """This function is used to show the image preview in the admin panel"""
        return mark_safe(f'<img src="{self.product.images.url}" width="50" />')
    
    class Meta:
        verbose_name = 'Product Variation'
        verbose_name_plural = 'Product Variations'
        ordering = ['-product', '-variation_category', '-size', '-color']
        abstract = True

class Product(Variation):
    """This class is used to create the product model"""
    product_name = models.CharField(max_length=200)
    size = models.ManyToManyField(ProductSize, related_name='products', blank=True)
    color = models.ManyToManyField(ProductColor, related_name='products', blank=True)
    sku = models.CharField(max_length=100, unique=True, editable=False, null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(ProductTags, related_name='products', blank=True)
    


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
    
    def save(self, *args, **kwargs):
        if not self.sku:
            # generate sku based on product name, category, and variation category
            sku_parts = [self.brand.name[:3], self.category.category_name[:3], self.variation_category.name[:3]]
            product_name_slug = slugify(self.product_name)
            self.sku = f'{product_name_slug}-{self.pk}-{"-".join(sku_parts)}'
        super().save(*args, **kwargs)

    # STEP 44: register the product model in the admin.py file of the store
