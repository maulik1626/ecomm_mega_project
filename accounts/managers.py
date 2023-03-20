# STEP 29: import the following modules

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

# STEP 30: make the AccountManager class and inherit BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, phone, password=None):
        if not email:
            raise ValueError(_("Users must have an email address"))
        if not username:
            raise ValueError(_("Users must have a username"))
        if not phone:
            raise ValueError(_("Users must have a phone number"))
        if not first_name:
            raise ValueError(_("Users must have a first name"))
        
        account = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            phone = phone,
        )
        
        account.set_password(password)
        account.save(using=self._db)
        return account
    
    def create_superuser(self, first_name, last_name, username, email, phone, password, **extra_fields):
        account = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone=phone,
            password=password,
        )
        account.is_staff = True
        account.is_superuser = True
        account.is_active = True
        account.is_admin = True
        account.save(using=self._db)
        return account

# STEP 31: go to models.py file and make the Accounts model