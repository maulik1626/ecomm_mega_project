# STEP 36: register Accounts it and run migrations
from django.contrib import admin
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
# STEP 37: customise appreance of the Account model's admin panel
# STEP 38: go to settings.py file and add media configurations for the images
class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'first_name', 'last_name', 'username', 'phone', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    list_filter = ('is_admin', 'is_staff', 'is_active', 'is_superuser')
        
    
    


admin.site.register(Account, AccountAdmin)
