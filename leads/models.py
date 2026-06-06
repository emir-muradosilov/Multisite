from django.db import models
from cities.models import City


# Create your models here.



class Lead(models.Model):

    STATUS_CHOICES = (
    ('new', 'Новая заявка'),
    ('target', 'Целевая'),
    ('spam', 'Спам'),
    ('no_answer', 'Не дозвон'),
)
    
    
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='leads'
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    service = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    utm_source = models.CharField(max_length=100, blank=True, null=True)
    utm_medium = models.CharField(max_length=100, blank=True, null=True)
    utm_campaign = models.CharField(max_length=100, blank=True, null=True)
    utm_term = models.CharField(max_length=255, blank=True, null=True)
    utm_content = models.CharField(max_length=255, blank=True, null=True)

    page_url = models.URLField(blank=True)
    ip_address = models.GenericIPAddressField(blank=True,   null=True)
    user_agent = models.TextField(blank=True, null=True)


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.city.name}"




