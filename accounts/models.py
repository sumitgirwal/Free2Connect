from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# Interest model
class Interest(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


# Custom user model
GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    country = models.CharField(max_length=255)
    interests = models.ManyToManyField(Interest)
    is_online = models.BooleanField(default=False)
    is_connected = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.username} | {self.full_name} | {self.email}"