from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        
        if email is None:
            raise ValueError("Email must not be blank")
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("staff user must be set to True")
        
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("super user must be set to True")
        
        
        user = self.create_user(email, password, **extra_fields)
        
        user.save()
        return user
    
    
             
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.SlugField(default="")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    
    def __str__(self):
        try:
            return f"{self.profile.first_name} {self.profile.last_name}"
        except:
            return self.email
    
    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name
  
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.CharField(max_length=1000, verbose_name=_("About yourself"))
    write_about = models.TextField(max_length=200, verbose_name=_("what you write about"))
    phone = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="profile", verbose_name=_("Profile Image"), default="uploads/brand.jpg")
    facebook_url = models.URLField(blank=True, null=True, verbose_name=_("Facebook url"), default="https://facebook.com" )
    instagram_url = models.URLField(blank=True, null=True, verbose_name=_("Instagram url"), default="https://instagram.com")
    twitter_url = models.URLField(blank=True, null=True, verbose_name=_("Twitter"), default="https://twiter.com")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name=_("LinkedIn"), default="https://linkedin.com")
   
    
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
