from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
import os

class AccountManager(BaseUserManager):

    def create_user(self, email, username, password=None, **other_fields):

        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        # user.is_active = True
        if other_fields.get('is_superuser') is not True:
            user.role = 2
        else:
            user.role = 1

        user.set_password(password)
        user.save() 

        return user
    
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError("is_staff must be set to True")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser must be set to True")
        
        return self.create_user(email, username, password, **other_fields)
    
    def create_admin(self, email, username, password=None):

        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        # user.is_active = True
        user.role = 1

        user.set_password(password)
        user.save() 

        return user


def get_account_image_upload_path(instance, filename):
    return os.path.join(
        'account_image',
        instance.username,
        filename
    )

# Create your models here.
class Account(AbstractBaseUser):

    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=254, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    mobile_number   = models.CharField(max_length=50, null=True)
    landline_number = models.CharField(max_length=50, null=True)
    address         = models.TextField(null=True)
    image           = models.ImageField(upload_to=get_account_image_upload_path, null=True)
    role            = models.IntegerField() # 1 - admin, 2 - user
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS  = ['email']

    objects = AccountManager()
    
