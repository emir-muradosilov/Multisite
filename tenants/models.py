from django.db import models
from cities.models import City
from users.models import User

# Create your models here.
class TenantProfile(models.Model):

    user = models.OneToOneField( User, on_delete=models.CASCADE, related_name='tenant_profile', verbose_name='Пользователь', )

    city = models.OneToOneField( City, on_delete=models.CASCADE, related_name='tenant_profile', verbose_name='Город',)

    company_name = models.CharField( max_length=255, blank=True, verbose_name='Имя организации', )

    address = models.CharField( max_length=255, blank=True, verbose_name='Адрес', )

    phone = models.CharField( max_length=30, blank=True, verbose_name='Телефон')

    phone_secondary = models.CharField( max_length=30, blank=True, verbose_name='Второй телефон',)

    working_hours = models.CharField(max_length=255, blank=True, verbose_name='Рабочее время', )

    email = models.EmailField( blank=True, verbose_name='email',)

    telegram = models.CharField( max_length=255, blank=True, verbose_name='Telegram')
    whatsapp = models.CharField(max_length=255,blank=True,verbose_name='Whatsapp')
    max = models.CharField(max_length=255,blank=True,verbose_name='Max')

#    website = models.URLField(blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.city.name} — {self.user.username}'