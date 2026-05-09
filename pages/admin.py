from django.contrib import admin
from django.utils.html import format_html

from .models import ServicePage, FAQ, CityData, ServiceTemplate


@admin.register(CityData)
class CityDataAdmin(admin.ModelAdmin):
    list_display = ('city',)
    search_fields = ('city__name',)


class ChildPageInline(admin.TabularInline):
    model = ServicePage
    fk_name = 'parent'
    extra = 0
    fields = ('title', 'slug', 'is_published')
    show_change_link = True


@admin.register(ServicePage)
class ServicePageAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'parent', 'is_published', 'show_in_menu', 'no_index', 'created_at', 'view_link')
    list_filter = ('city', 'is_published','show_in_menu','no_index',)
    search_fields = ('title', 'slug', 'content', 'seo_title',)

    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ('city', 'parent')

    inlines = [ChildPageInline]

    fieldsets = (
        ('Основное', {
            'fields': (
                'city',
                'parent',
                'title',
                'slug',
            )
        }),

        ('Контент', {
            'fields': (
                'content',
            )
        }),

        ('SEO', {
            'fields': (
                'seo_title',
                'seo_description',
                'seo_keywords',
            )
        }),

        ('Настройки', {
            'fields': (
                'is_published',
                'show_in_menu',
                'no_index',
            )
        }),
    )

    ordering = ('city', 'parent', 'title')

    def view_link(self, obj):
        if obj.parent:
            url = f"/{obj.city.slug}/{obj.parent.slug}/{obj.slug}/"
        else:
            url = f"/{obj.city.slug}/{obj.slug}/"

        return format_html('<a href="{}" target="_blank">Открыть</a>', url)

    view_link.short_description = "Страница"


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):

    list_display = ('question', 'city', 'created_at', 'view_link')
    list_filter = ('city',)
    search_fields = ('question', 'answer')

    prepopulated_fields = {"slug": ("question",)}

    def view_link(self, obj):
        url = f"/{obj.city.slug}/faq/{obj.slug}/"
        return format_html('<a href="{}" target="_blank">Открыть</a>', url)

    view_link.short_description = "Страница"



admin.site.register(ServiceTemplate)






