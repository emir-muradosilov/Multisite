from django.db import models
from cities.models import City


class ServicePage(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='service_pages'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField()

    content = models.TextField()

    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ✅ SEO статусы
    is_published = models.BooleanField(default=True)
    show_in_menu = models.BooleanField(default=True)
    no_index = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'parent', 'slug'],
                name='unique_city_parent_slug'
            )
        ]

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
    seo_keywords = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['city', 'slug'], name='unique_city_faq_slug')
        ]

    def __str__(self):
        return self.question


class CityData(models.Model):
    city = models.OneToOneField(City, on_delete=models.CASCADE)

    industrial_zones = models.TextField(blank=True)
    districts = models.TextField(blank=True)

    typical_concrete = models.CharField(max_length=100, blank=True)
    typical_thickness = models.CharField(max_length=100, blank=True)

    price_range = models.CharField(max_length=100, blank=True)
    competitors = models.TextField(blank=True)

    portfolio = models.TextField(blank=True)
    restrictions = models.TextField(blank=True)

    def __str__(self):
        return f"SEO данные — {self.city.name}"
    

class ServiceTemplate(models.Model):
    title_template = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    content_template = models.TextField()

    seo_title_template = models.CharField(max_length=255)
    seo_description_template = models.TextField()

    seo_keywords_template = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.slug




