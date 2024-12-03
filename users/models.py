from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from datetime import timedelta
from PIL import Image


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('admin', 'Admin'),
    ], default='student')
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    def is_otp_valid(self):
        if self.otp_created_at:
            return now() <= self.otp_created_at + timedelta(minutes=5)
        return False

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", default="profile_pics/default.jpg")
    
    
    def __str__(self):
        return f"{self.user.email} Profile"




