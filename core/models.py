from django.db import models

class SiteSettings(models.Model):

    site_name = models.CharField( max_length=255, default='Алмазное бурение')
    default_phone = models.CharField( max_length=30, blank=True)
    logo = models.ImageField( upload_to='site/', blank=True, null=True)
    favicon = models.ImageField( upload_to='site/', blank=True, null=True)
    homepage_title = models.CharField( max_length=255, blank=True )
    homepage_description = models.TextField( blank=True)
    homepage_keywords = models.TextField(blank=True)
    hero_background = models.ImageField( upload_to='hero/', blank=True, null=True)

    homepage_text_h2 = models.CharField( blank=True)
    homepage_text = models.TextField( blank=True)
    homepage_advantages_h2 = models.CharField( blank=True)
    homepage_advantages = models.TextField( blank=True)


    class Meta:
        verbose_name = 'Настройка сайта'          # единственное число
        verbose_name_plural = 'Настройки сайта'   # множественное
        db_table = 'site_settings'             # опционально: явное имя таблицы


    def __str__(self):
        return 'Настройки сайта'
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)



class PriceTable(models.Model):

    settings = models.ForeignKey( SiteSettings, on_delete=models.CASCADE, related_name='price_tables')
    title = models.CharField(max_length=255)
    service_column_name = models.CharField( max_length=100, default='Услуга')
    unit_column_name = models.CharField( max_length=100, default='Ед. изм.')
    price_column_name = models.CharField(max_length=100, default='Цена')
    sort_order = models.PositiveIntegerField( default=0)

    show_unit = models.BooleanField(default=True)
    show_price = models.BooleanField(default=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title



class PriceTableItem(models.Model):

    table = models.ForeignKey( PriceTable, on_delete=models.CASCADE, related_name='items')
    service = models.CharField( max_length=255,)
    unit = models.CharField( max_length=100, blank=True, )
    price = models.CharField( max_length=100,)
    sort_order = models.PositiveIntegerField( default=0)




class WorkType(models.Model):

    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )

    image = models.ImageField(
        upload_to='work-types/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )

    button_text = models.CharField(
        max_length=100,
        default='Оставить заявку',
        verbose_name='Текст кнопки'
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Выполняемая работа'
        verbose_name_plural = 'Выполняемые работы'

    def __str__(self):
        return self.title

