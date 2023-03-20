from django.contrib import admin
from store.models import Product
# Register your models here.

# STEP 45: make admin class for the product model and register it
class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ['product_name', 'category', 'price', 'stock', "is_available", "modified_date", 'img_preview']
    readonly_fields = ['img_preview']
    list_filter = ['category']
    prepopulated_fields = {'slug': ("product_name",)}
    

admin.site.register(Product, ProductAdmin)

# STEP 46: make migrations and migrate
# STEP 47: add some products in the admin panel and then go to ecomm_project/views.py and create a function to show the products in the home page