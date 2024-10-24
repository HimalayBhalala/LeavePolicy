from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils.translation import gettext_lazy as _

# Create your models here.

ROLE_CHOOSES = [
    ("admin","Admin"),
    ("hr","Hr"),
    ("pm","Pm"),
    ("tl","Tl"),
    ("developer","Developer")
]

class User(AbstractBaseUser,PermissionsMixin):
    first_name = models.CharField(_("First Name"),max_length=200,null=True,blank=True)
    last_name = models.CharField(_("Last Name"),max_length=200,null=True,blank=True)
    username = models.CharField(_("Username"),null=True,blank=True)
    email = models.EmailField(_("Email"),max_length=200,unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=ROLE_CHOOSES)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["role"]

    def __str__(self):
        return f"{self.email}"