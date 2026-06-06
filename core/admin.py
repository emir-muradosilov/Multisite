from django.contrib import admin


from django.contrib import admin

from .models import (
    SiteSettings,
    PriceTable,
    PriceTableItem,
    WorkType
)


class PriceTableItemInline(admin.TabularInline):

    model = PriceTableItem
    extra = 1
    ordering = ['sort_order']
    fields = [
        'service',
        'unit',
        'price',
        'sort_order'
    ]

@admin.register(PriceTable)
class PriceTableAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'sort_order'
    ]
    ordering = ['sort_order']
    inlines = [PriceTableItemInline]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):


    fieldsets = (
        ( 'Основные', {'fields': ('site_name', 'default_phone', 'logo', 'favicon', 'hero_background',)}),
        ('SEO главной страницы',{ 'fields': ('homepage_title', 'homepage_description','homepage_keywords','homepage_text_h2','homepage_text','homepage_advantages_h2', 'homepage_advantages',) }),
    )


    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()




@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'sort_order',
        'is_published'
    )

    list_editable = (
        'sort_order',
        'is_published'
    )

    search_fields = (
        'title',
        'description'
    )




