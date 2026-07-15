from django.db import models
from slugify import slugify
# Create your models here.

class City(models.Model):

    name = models.CharField(max_length=100, unique=True)
    name_where = models.CharField(max_length=100, unique=True)
    name_oblast = models.CharField(max_length=100, unique=True)
    name_oblast_where = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=200, unique=True, blank=True)
#    subdomain = models.CharField(max_length=100, unique=True)

    is_active = models.BooleanField(default=True)
    is_rented = models.BooleanField(default=False)

    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    price_text = models.CharField(max_length=255, blank=True, null=True)

    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)

    h1_title = models.CharField(max_length=255, blank=True, null=True)

    rent_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rented_until = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)

    page_score = models.IntegerField(default=0)

    is_main = models.BooleanField(default=False,verbose_name='Главный город')


    choose_as_h2 = models.TextField( blank=True)
    choose_as = models.TextField( blank=True)

    useful_h2 = models.TextField( blank=True)
    useful = models.TextField( blank=True)

    homepage_text_h2 = models.TextField( blank=True)
    homepage_text = models.TextField( blank=True)

    homepage_advantages_h2 = models.TextField( blank=True)
    homepage_advantages = models.TextField( blank=True)



    def get_absolute_url(self):

        if self.is_main:
            return '/'

        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def in_city(self):
        return self.name_where


    @property
    def oblast(self):
        return self.name_oblast


    @property
    def in_oblast(self):
        return self.name_oblast_where

