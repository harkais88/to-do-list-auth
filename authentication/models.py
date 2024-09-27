from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=255,null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} Email:{self.email} Status:{self.is_active} \n \
                Created At: {self.created_at} Updated At: {self.updated_at}"