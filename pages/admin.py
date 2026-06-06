from django.contrib import admin
from django.utils.html import format_html

from .models import ServicePage, FAQ, CityData, ServiceTemplate, SEOBlock, PortfolioCase, Review, DistrictPageTemplate, ServiceTemplatePrice, GlobalFAQ


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


class ServicePriceInline(admin.TabularInline):

    model = ServiceTemplatePrice
    extra = 1

    

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
    filter_horizontal = ('related_services',)

    fieldsets = (
    ('SEO', {
        'fields': (
            'seo_title',
            'seo_description',
            'seo_keywords',
            'h1_title',
        )
    }),
)

    def view_link(self, obj):
        url = f"/{obj.city.slug}/faq/{obj.slug}/"
        return format_html('<a href="{}" target="_blank">Открыть</a>', url)

    view_link.short_description = "Страница"

@admin.register(ServiceTemplate)
class ServiceTemplateAdmin(admin.ModelAdmin):

    list_display = ('title_template', 'slug', 'parent', 'show_in_menu', 'is_main')
    list_display_links = ('title_template',)
    list_editable  = ( 'slug', 'parent', 'show_in_menu', 'is_main')
    
    inlines = [ServicePriceInline]




@admin.register(SEOBlock)
class SEOBlockAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'block_type',
        'is_active',
        'sort_order',
    )

    list_filter = (
        'block_type',
        'is_active',
    )

    search_fields = (
        'title',
        'content',
    )

    filter_horizontal = (
        'services',
        'cities',
    )

@admin.register(PortfolioCase)
class PortfolioCaseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'city',
        'service_page',
        'district',
        'is_published',
    )

    list_filter = (
        'city',
        'is_published',
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    search_fields = (
        'title',
        'object_name',
        'address',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'author',
        'city',
        'rating',
        'is_published'
    )

    list_filter = (
        'city',
        'rating',
        'is_published'
    )

    search_fields = (
        'author',
        'text'
    )

    filter_horizontal = (
        'related_services',
    )


@admin.register(DistrictPageTemplate)
class DistrictPageTemplateAdmin(admin.ModelAdmin):

    list_display = (
        'service_template',
        'is_active'
    )

    list_filter = (
        'is_active',
    )



@admin.register(GlobalFAQ)
class GlobalFAQAdmin(admin.ModelAdmin):

    list_display = (
        'question',
        'sort_order',
        'is_published'
    )

    list_editable = (
        'sort_order',
        'is_published'
    )

    search_fields = (
        'question',
        'answer'
    )

    ordering = (
        'sort_order',
    )








