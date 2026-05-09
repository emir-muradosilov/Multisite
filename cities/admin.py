from django.contrib import admin
from .models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "is_active", "is_rented")
    list_filter = ("is_active", "is_rented")
    search_fields = ("name", "slug", "seo_title", "h1_title")
    fieldsets = (
        ("Основное", {"fields": ("name", "slug", "is_active", "is_rented")}),
        ("Контакты", {"fields": ("phone", "address", "price_text", "telegram_chat_id")}),
        ("SEO главной страницы города", {"fields": ("h1_title", "seo_title", "seo_description", "seo_keywords")}),
        ("Аренда", {"fields": ("rent_price", "rented_until")}),
    )

