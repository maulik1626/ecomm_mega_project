from category.models import Category

# STEP 57: add the category_list function to the ecomm_project/settings.py file in the TEMPLATES list
def category_list(request):
    """This function is used to show the categories in the store page and make it accessible anywhere into the project"""
    links = Category.objects.all()
    return dict(category_links=links)