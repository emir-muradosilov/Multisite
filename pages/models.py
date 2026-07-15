from django.db import models
from cities.models import City
from slugify import slugify
from pages.services.images import (
    convert_to_webp,
    generate_seo_filename
)


class ServiceTemplate(models.Model):
    title_template = models.CharField(max_length=255)

    slug = models.SlugField(max_length=200, unique=True)

    content_template = models.TextField()

    seo_title_template = models.CharField(max_length=255)
    seo_description_template = models.TextField()

    seo_keywords_template = models.TextField(blank=True, null=True)

    h1_template = models.CharField(max_length=255)

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    show_in_menu = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    
    def __str__(self):
        return self.slug


class District(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='districts'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    population = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ServiceTemplatePrice(models.Model):

    template = models.ForeignKey(
        ServiceTemplate,
        on_delete=models.CASCADE,
        related_name='prices'
    )

    title = models.CharField(
        max_length=255
    )

    unit = models.CharField(
        max_length=100,
        blank=True
    )

    price = models.CharField(
        max_length=100
    )

    sort_order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class ServicePage(models.Model):
    city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='service_pages'    )

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=False)

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

    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    h1_title = models.CharField(max_length=255,blank=True,null=True)


    district = models.ForeignKey('District',on_delete=models.CASCADE,null=True,blank=True,related_name='pages')

    template = models.ForeignKey(ServiceTemplate, on_delete=models.SET_NULL, null=True, blank=True, related_name='pages')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['city', 'parent', 'slug'],
                name='unique_city_parent_slug'
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.city.name}"
    
    
    
    def get_absolute_url(self):

        is_main_city = self.city.is_main

        # дочерняя страница
        if self.parent:

            if is_main_city:
                return f"/{self.parent.slug}/{self.slug}/"

            return f"/{self.city.slug}/{self.parent.slug}/{self.slug}/"

        # родительская страница
        if is_main_city:
            return f"/{self.slug}/"

        return f"/{self.city.slug}/{self.slug}/"
    



    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SEOBlock(models.Model):

    BLOCK_TYPES = (
        ('text', 'Text'),
        ('cta', 'CTA'),
        ('trust', 'Trust'),
        ('price', 'Price'),
        ('review', 'Review'),
    )

    title = models.CharField(max_length=255)

    block_type = models.CharField(
        max_length=50,
        choices=BLOCK_TYPES,
        default='text'
    )

    content = models.TextField()

    services = models.ManyToManyField(
        ServicePage,
        blank=True,
        related_name='seo_blocks'
    )

    cities = models.ManyToManyField(
        City,
        blank=True,
        related_name='seo_blocks'
    )

    is_active = models.BooleanField(default=True)

    sort_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return self.title


class FAQ(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="faqs",
        null=True,
        blank=True,
    )

    question = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, blank=True)
    answer = models.TextField()
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    seo_description = models.TextField(blank=True, null=True)
    seo_keywords = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    h1_title = models.CharField(max_length=255, blank=True, null=True)
    related_services = models.ManyToManyField(ServicePage, blank=True, related_name='related_faqs')


    def get_absolute_url(self):

        if self.city.is_main:
            return f"/faq/{self.slug}/"

        return f"/{self.city.slug}/faq/{self.slug}/"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['city', 'slug'], name='unique_city_faq_slug')
        ]

    def __str__(self):
        return self.question


class FAQTemplate(models.Model):

    question_template = models.CharField(max_length=255)
    answer_template = models.TextField()
    slug = models.SlugField(unique=True)
    related_service_templates = models.ManyToManyField(ServiceTemplate,blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.question_template)

        super().save(*args, **kwargs)



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

    metro = models.TextField(blank=True)
    streets = models.TextField(blank=True)
    business_centers = models.TextField(blank=True)
    residential_complexes = models.TextField(blank=True)

    def __str__(self):
        return f"SEO данные — {self.city.name}"
    



class DistrictPageTemplate(models.Model):

    service_template = models.ForeignKey(
        ServiceTemplate,
        on_delete=models.CASCADE,
        related_name='district_templates'
    )

    title_template = models.CharField(
        max_length=255
    )

    h1_template = models.CharField(
        max_length=255
    )

    content_template = models.TextField()

    seo_title_template = models.CharField(
        max_length=255,
        blank=True
    )

    seo_description_template = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.service_template.title_template


class PortfolioCase(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='portfolio_cases'
    )

    service_page = models.ForeignKey(
        ServicePage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio_cases'
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio_cases'
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField()

    short_description = models.TextField()

    content = models.TextField()

    object_name = models.CharField(
        max_length=255,
        blank=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    work_duration = models.CharField(
        max_length=100,
        blank=True
    )

    price = models.CharField(
        max_length=100,
        blank=True
    )

    image = models.ImageField(
        upload_to='portfolio/',
        blank=True,
        null=True
    )

    seo_title = models.CharField(
        max_length=255,
        blank=True
    )

    seo_description = models.TextField(
        blank=True
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):

        return (
            f"/{self.city.slug}/"
            f"cases/"
            f"{self.slug}/"
        )
    

    def save(self, *args, **kwargs):
        if self.image:

            self.image = convert_to_webp(
                self.image
            )
            self.image.name = generate_seo_filename(
                title=self.title,
                city=self.city.name
            )
        super().save(*args, **kwargs)


class Review(models.Model):

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )

    related_services = models.ManyToManyField(
        ServicePage,
        blank=True,
        related_name='reviews'
    )

    author = models.CharField(max_length=255)

    text = models.TextField()

    rating = models.PositiveSmallIntegerField(default=5)

    source = models.CharField(
        max_length=255,
        blank=True
    )

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', '-created_at']

    def __str__(self):
        return f"{self.author} ({self.rating}/5)"


class DistrictServicePage(models.Model):

    city = models.ForeignKey(City,on_delete=models.CASCADE)
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    service_page = models.ForeignKey(ServicePage,on_delete=models.CASCADE)
    seo_title = models.CharField(max_length=255,blank=True)
    seo_description = models.TextField(blank=True)
    content = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:

        unique_together = (
            'district',
            'service_page',
        )

    def __str__(self):

        return (
            f'{self.service_page.title} — '
            f'{self.district.name}'
        )

    def get_absolute_url(self):

        return (
            f'/{self.city.slug}/'
            f'districts/'
            f'{self.district.slug}/'
            f'{self.service_page.slug}/'
        )


class GlobalFAQ(models.Model):

    question = models.CharField(
        max_length=255,
        verbose_name='Вопрос'
    )

    answer = models.TextField(
        verbose_name='Ответ'
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликован'
    )

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'FAQ главной страницы'
        verbose_name_plural = 'FAQ главной страницы'

    def __str__(self):
        return self.question



class TopMenuItem(models.Model):

    title = models.CharField(
        max_length=100,
        verbose_name="Название"
    )

    url = models.CharField(
        max_length=255,
        verbose_name="URL"
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Показывать"
    )

    def get_absolute_url(self, city=None):

        if city and not city.is_main:
            return f"/{city.slug}/{self.url}/"

        return f"/{self.url}/"

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Верхнее меню"
        verbose_name_plural = "Верхнее меню"

    def __str__(self):
        return self.title


