from django.db import models
from django.utils.text import slugify
from category.models import Category
from django.utils.html import mark_safe
from django.urls import reverse

from math import ceil
from model_clone import CloneMixin

# Create your models here.
class ProductBrand(models.Model):
    """This class is used to create the product brand model"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Brand'
        verbose_name_plural = 'Product Brands'

class ProductType(models.Model):
    """This class is used to create the product type model"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

class ProductTags(models.Model):
    name = models.CharField(max_length=200, unique=True)
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

class Variation(CloneMixin, models.Model):
    
    product_name = models.CharField(max_length=200)
    variation_name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, null=True, blank=True)
    images = models.ImageField(upload_to='photos/products/variations', null=True, blank=True)
    stock = models.IntegerField()
    price = models.IntegerField()
    discount = models.IntegerField(default=0, blank=True, null=True)
    discount_price = models.IntegerField(default=0, blank=True, null=True)
    
    
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    sku = models.CharField(max_length=100, editable=False, null=True, blank=True, unique=True)
    description = models.TextField(blank=True)

    # product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True)
    # variation_category = models.ForeignKey(ProductVariationCategory, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.product_name
    
    def img_preview(self):
        """This function is used to show the image preview in the admin panel"""
        return mark_safe(f'<img src="{self.images.url}" width="50" />')
    
    # def get_url(self):
    #     """This function is used to get the absolute url of the product"""
    #     return reverse("product_detail", args=[self.category.slug, self.slug])
    
    def save(self, *args, **kwargs):
        """This function is used to generate the sku and slug of the product"""
        if self.discount > 0:
            self.discount_price = ceil(self.price - (self.price * (self.discount / 100)))
            
        self.product_name = str(self.color.color_name) + ' ' + str(self.product.product_name)
        
        self.variation_name = str(self.color.color_name) + ' ' + str(self.product.product_name) + '-' + str(self.size.name)

        sku_parts = ['-size-', self.size.name, '-color-', self.color.color_name]
        product_name_slug = slugify(self.variation_name)
        product_brand_name_slug = slugify(self.product.brand.name)
        self.sku = f'{product_brand_name_slug}-{product_name_slug}-{"-".join(sku_parts)}'
        
        self.description =  str(self.color.color_name) + ' ' + str(self.product.brand.name) + ' ' + str(self.product_name) + ' ' + str(self.product.category.category_name) + ' for men'
        
        if self.stock >= 1:
            self.is_available = True
        else:
            self.is_available = False

        super().save(*args, **kwargs)
    
    def get_color_hex(self):
        return self.color.color_hex
    
    def get_size(self):
        return self.size.name
    
    
    def get_color_url(self):
        """This function is used to get the absolute url of the product"""
        return reverse("soft_get_product_by_color", args=[self.color.id, self.product.category.slug, self.product.slug])
    
    def get_url(self):
        """This function is used to get the absolute url of the product"""
        return reverse("product_detail", args=[self.product.category.slug, self.product.slug, self.color.id])

    
    class Meta:
        verbose_name = 'Product Variation'
        verbose_name_plural = 'Product Variations'
        ordering = ['-product', '-product_name', '-size', '-color']

class Product(models.Model):
    """This class is used to create the product model"""
    product_name = models.CharField(max_length=200)
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    images = models.ImageField(upload_to='photos/products')
    tags = models.ManyToManyField(ProductTags, related_name='products', blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, null=True, blank=True)
    
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
    
    
    def get_color_hex(self):
        return self.color.color_hex

    # STEP 44: register the product model in the admin.py file of the store
