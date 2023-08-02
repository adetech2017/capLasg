from django.db import models
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    is_accreditor = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    # Any additional fields you might want to add
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # Set the username to the email address
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username


class Status(models.Model):
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status


class Category(models.Model):
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.category