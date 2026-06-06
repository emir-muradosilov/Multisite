from django.db import models
from cities.models import City
from users.models import User

# Create your models here.
class TenantProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tenant_profile'
    )

    city = models.OneToOneField(
        City,
        on_delete=models.CASCADE,
        related_name='tenant_profile'
    )

    company_name = models.CharField(
        max_length=255,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    phone_secondary = models.CharField(
        max_length=30,
        blank=True
    )

    working_hours = models.CharField(
        max_length=255,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    telegram = models.CharField(
        max_length=255,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=255,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f'{self.city.name} — {self.user.username}'