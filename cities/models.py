from django.db import models

# Create your models here.

class City(models.Model):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    subdomain = models.CharField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)
    is_rented = models.BooleanField(default=False)

    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    rent_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rented_until = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

