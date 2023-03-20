# STEP 32: Make the Accounts model

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from accounts.managers import AccountManager

# Create your models here.
class Account(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, unique=True)

    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "phone"]
    
    objects = AccountManager()
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label: str) -> bool:
        return True
    
# STEP 33: reguster the customUserModel into the settings.py file to use it. 