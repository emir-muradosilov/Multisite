from django.db import models
from django.contrib.auth.models import AbstractUser
from cities.models import City


# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('tenant', 'Tenant'),
        ('manager', 'Manager'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='tenant')
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants')

    

    def __str__(self):
        return self.username

