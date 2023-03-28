from django.contrib import admin
from django.utils.html import mark_safe
from store.models import Product, ProductBrand, ProductType, ProductTags, ProductColor, ProductVariationCategory, ProductSize
# Register your models here.

# STEP 45: make admin class for the product model and register it
class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ['brand', 'product_name', 'category', 'color_preview', 'price', 'discount', 'discount_price', 'stock', "modified_date", 'img_preview', "is_available"]
    readonly_fields = ['img_preview', "sku", "modified_date", "created_date", 'discount_price']
    list_filter = [ 'brand', 'category', 'is_available', "modified_date", "created_date"]
    prepopulated_fields = {'slug': ("product_name",)}
    list_editable = ['is_available', "stock", 'discount']
    list_display_links = ['brand', 'product_name']

    filter_horizontal = ['tags', 'size']
    search_fields = ['product_name', 'description']
    fieldsets = (
        ('Product Information', {
            'fields': ('brand', 'product_name', 'product_type',  'category', 'variation_category', 'size', 'color' , 'stock', 'slug', 'description', 'is_available')
        }),
        ('Product Price Information', {
            'fields': ('price', 'discount', 'discount_price')
        }),
        ('Image Information', {
            'fields': ("img_preview", 'images')
        }),
        ('Tag Information', {
            'fields': ('tags',)
        }),
        ('Other Information', {
            'fields': ('sku', "modified_date", "created_date")
        }),
    )


    # Define the add_fieldsets to use in the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product_name', 'description', 'category', 'price', 'stock', 'is_available', 'images', 'tags', 'brand', 'product_type', 'variation_category', 'color', 'size')
        }),
    )
    
    def color_preview(self, obj):
        if obj.color:
            return mark_safe(f'<div style="width: 50px; height: 20px; background-color: {obj.color.color_hex}"></div>')
        else:
            return '-'
    
    # def size_preview(self, obj):
    #     if obj.size:
    #         print(f"\n\n\n{obj}\n\n\n")
    #         print(f"\n\n\n{obj.size}\n\n\n")
    #         print(f"\n\n\n{obj.size.name}\n\n\n")
    #     return '-'

    
    color_preview.allow_tags = True
    color_preview.short_description = 'Color Preview'

    # size_preview.allow_tags = True
    # size_preview.short_description = 'Available Sizes'

class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('color_name', 'color_hex', 'color_preview')
    ordering = ('color_name', 'color_hex')
    list_display_links = ("color_preview",)

    def color_preview(self, obj):
        return mark_safe(f'<div style="width: 50px; height: 20px; background-color: {obj.color_hex}"></div>')

    color_preview.allow_tags = True
    color_preview.short_description = 'Color Preview'


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register([ProductBrand, ProductType, ProductTags, ProductVariationCategory, ProductSize])



# STEP 46: make migrations and migrate
# STEP 47: add some products in the admin panel and then go to ecomm_project/views.py and create a function to show the products in the home page




# class VariationAdmin(admin.ModelAdmin):
#     model = Variation

#     list_display = ['product', 'variation_category', 'variation_value', 'is_active', 'img_preview']
#     list_filter = ['variation_category', 'variation_value', 'is_active']
#     list_editable = ['is_active']