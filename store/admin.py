from django.contrib import admin
from django.utils.html import mark_safe
from store.models import Product, ProductBrand, ProductType, ProductTags, ProductColor, ProductVariationCategory, ProductSize, Variation

# Register your models here.

# STEP 45: make admin class for the product model and register it

class VariationInline(admin.TabularInline):
    model = Variation
    fields = ("product_name","size","color", "color_preview","images","stock","price","discount","discount_price", "img_preview", "is_available")
    readonly_fields = ("discount_price",'color_preview', "img_preview", 'product_name')
    extra = 1
    list_display_links = ['product_name']
    
    def color_preview(self, obj):
        if obj.color:
            return mark_safe(f'<div style="width: 50px; height: 20px; background-color: {obj.color.color_hex}"></div>')
        else:
            return '-'
    color_preview.allow_tags = True
    color_preview.short_description = 'Color Preview'
    
    def img_preview(self, obj):
        if obj.color:
            return mark_safe(f'<img src="{obj.images.url}" width="50" />')
        else:
            return '-'    
    img_preview.allow_tags = True
    img_preview.short_description = 'Image Preview'

class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = ['brand', 'product_name', 'product_type', 'category', "modified_date", 'img_preview', "is_available"]

    readonly_fields = ['img_preview', "modified_date", "created_date"]

    list_filter = [ 'brand', 'product_name', 'category', 'is_available', "modified_date", "created_date"]

    prepopulated_fields = {'slug': ("product_name",)}

    list_editable = ['is_available']

    list_display_links = ['brand', 'product_name', 'img_preview']

    filter_horizontal = ['tags']

    search_fields = ['product_name', 'brand', 'category', 'tags']
    
    inlines = [VariationInline]
    
    fieldsets = (
        ('Product Information', {
            'fields': ('brand', 'product_name', 'product_type', 'category', 'slug', 'is_available')
        }),
        ('Images', {
            'fields': ("img_preview", 'images')
        }),
        ('Tag Information', {
            'fields': ('tags',)
        }),
        ('Other Information', {
            'fields': ("modified_date", "created_date")
        }),
    )


    # # Define the add_fieldsets to use in the add form
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('product_name', 'category', 'is_available', 'images', 'tags', 'brand')
    #     }),
    # )
    
    def color_preview(self, obj):
        if obj.color:
            return mark_safe(f'<div style="width: 50px; height: 20px; background-color: {obj.color.color_hex}"></div>')
        else:
            return '-'
    color_preview.allow_tags = True
    color_preview.short_description = 'Color Preview'

class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'color_name', 'color_hex', 'color_preview')
    ordering = ('color_name', 'color_hex')
    list_display_links = ("color_preview",)
    search_fields = ('id', 'color_name', 'color_hex')

    def color_preview(self, obj):
        return mark_safe(f'<div style="width: 50px; height: 20px; background-color: {obj.color_hex}"></div>')

    color_preview.allow_tags = True
    color_preview.short_description = 'Color Preview'


class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
class ProductTagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
class ProductVariationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'product_variation_category')
    list_filter = ('product_variation_category',)

# STEP 46: make migrations and migrate
# STEP 47: add some products in the admin panel and then go to ecomm_project/views.py and create a function to show the products in the home page

class VariationAdmin(admin.ModelAdmin):
    model = Variation

    list_display = ['variation_name', 'product', 'color', 'color_preview', 'size', 'price', 'discount', 'discount_price', 'stock', 'img_preview', 'is_available']
    
    readonly_fields = ['img_preview', 'sku', "modified_date", "created_date", 'discount_price']
    
    list_filter = [ 'product_name', 'product', 'size', 'discount', 'is_available', "modified_date", "created_date"]
    
    list_editable = ['is_available', "stock", 'discount']
    
    list_display_links = ['product', 'variation_name', 'img_preview']

    search_fields = ['product_name', 'product', 'size', 'discount']

    fieldsets = (
        ('Product Information', {
            'fields': ('product',  'size', 'color', 'stock', 'description', 'is_available')
        }),
        ('Product Price Information', {
            'fields': ('price', 'discount', 'discount_price')
        }),
        ('Image Information', {
            'fields': ("img_preview", 'images')
        }),
        ('Other Information', {
            'fields': ('sku', "modified_date", "created_date")
        }),
    )

    # Define the add_fieldsets to use in the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('product_name', 'product', 'description', 'price', 'stock', 'is_available', 'images', 'color', 'size')
        }),
    )
    
    def color_preview(self, obj):
        if obj.color:
            return mark_safe(f'<div style="width: 50px; height: 20px; background-color: {obj.color.color_hex}"></div>')
        else:
            return '-'
    color_preview.allow_tags = True
    color_preview.short_description = 'Color Preview'




admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductTags, ProductTagsAdmin)
admin.site.register(ProductVariationCategory, ProductVariationCategoryAdmin)
admin.site.register(ProductSize, ProductSizeAdmin)