from django.db import models
from cities.models import City


# Create your models here.

class ServicePage(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='service_pages'
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField()

    content = models.TextField()

    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.city.name}"


class FAQ(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='faqs'
    )

    question = models.CharField(max_length=255)
    slug = models.SlugField()

    answer = models.TextField()

    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question