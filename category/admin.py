from django.contrib import admin

# STEP 25: import the category models
from category.models import Category

# Register your models here.
# STEP 42: Add CategoryAdmin class and register it
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug', "img_preview"]
    readonly_fields = ['img_preview']
    prepopulated_fields = {'slug': ('category_name',)}


admin.site.register(Category, CategoryAdmin)



# STEP 26: run makemigrations and migtare
# STEP 27: Make a custom user model now. make an accounts app
# STEP 28: Make a file named managers.py in the accounts app to make the accounts manager class

# STEP 43: make a store app and go to models.py file of the store app