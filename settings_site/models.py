from django.db import models


class SiteSettings(models.Model):

    # =========================
    # BASIC
    # =========================

    site_name = models.CharField(
        max_length=255,
        default='Алмазное бурение'
    )

    logo = models.ImageField(
        upload_to='site/',
        blank=True,
        null=True
    )

    default_phone = models.CharField(
        max_length=30,
        blank=True
    )

    default_address = models.CharField(
        max_length=255,
        blank=True
    )

    # =========================
    # SEO HOMEPAGE
    # =========================

    homepage_title = models.CharField(
        max_length=255,
        blank=True
    )

    homepage_description = models.TextField(
        blank=True
    )

    homepage_keywords = models.TextField(
        blank=True
    )

    # =========================
    # CONTACTS
    # =========================

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

    # =========================
    # Analitics
    # =========================

    robots_index = models.BooleanField(default=True)
    yandex_verification = models.CharField(max_length=255, blank=True)
    google_verification = models.CharField(max_length=255, blank=True)
    default_og_image = models.ImageField(upload_to='site/', blank=True,null=True)


    # =========================
    # SYSTEM
    # =========================

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return 'Настройки сайта'

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'