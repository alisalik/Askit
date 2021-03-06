from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class UserProfileManager(BaseUserManager):

    def create_user(self,email,name,password=None):
        if not email:
            raise ValueError("User must have a valid email")
        email=self.normalize_email(email)
        user= self.model(email=email,name=name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,name,password):
        user = self.create_user(email,name,password)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    uutoken = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(unique=True)
    name= models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    country= models.CharField(max_length=100)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects=UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS= ['name']

    def __str__(self):
        return self.name
