from django.contrib import admin
from .models import City
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from pages.models import ServicePage
from pages.services.page_quality import calculate_page_score
from cities.forms import CityAdminForm

from cities.forms import CityAdminForm

from cities.services.copy_city_structure import (
    copy_city_structure
)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    form = CityAdminForm

    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        "name", "slug", "is_active", 'is_main', "is_rented", "tenant_name", "tenant_phone", "leads_count", 'rent_price', "rent_expire_date","seo_score","indexed_pages","noindex_pages","weak_pages",)
    list_filter = ("is_active", "is_rented", 'is_main',)
    search_fields = ("name", "slug", "seo_title", "h1_title")
    fieldsets = (
        ("Основное", {"fields": ("name", "slug", 'name_where', 'name_oblast', 'name_oblast_where', "is_active", "is_rented")}),
        ("Копирование", {"fields": ("copy_structure",)}),
        ("Контакты", {"fields": ("phone", "address", "price_text", "telegram_chat_id")}),
        ("SEO главной страницы города", {"fields": ("h1_title", "seo_title", "seo_description", "seo_keywords")}),
        ("Аренда", {"fields": ("rent_price", "rented_until")}),
    )

    list_editable  = ( 'rent_price', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(leads_total=Count('leads'))
        return queryset.select_related(
            'tenant_profile',
            'tenant_profile__user',
        )

    def rent_status(self, obj):

        if not obj.is_rented:
            return 'Свободен'

        if not obj.rented_until:
            return 'Арендован'

        today = timezone.now().date()

        if obj.rented_until < today:
            return 'Истёк срок'

        if obj.rented_until <= today + timedelta(days=7):
            return 'Истекает скоро'

        return 'Арендован'

    rent_status.short_description = 'Статус'

    def rent_expire_date(self, obj):
        if obj.rented_until:
            return obj.rented_until.strftime(
                '%d.%m.%Y'
            )
        return '—'

    rent_expire_date.short_description = 'Оплачено до'


    def tenant_name(self, obj):
        tenant = getattr(obj,'tenant_profile', None)
        if tenant:
            return tenant.user.username
        return '—'
    tenant_name.short_description = 'Арендатор'


    def tenant_phone(self, obj):
        tenant = getattr(obj, 'tenant_profile', None)
        if tenant and tenant.phone:
            return tenant.phone
        return '—'
    tenant_phone.short_description = 'Телефон'


    def leads_count(self, obj):
        return obj.leads_total
    leads_count.short_description = 'Заявки'


    def seo_score(self, obj):
        pages = ServicePage.objects.filter( city=obj, is_published=True)
        scores = []
        for page in pages:
            score = calculate_page_score(
                page,
                {
                    'faqs': [],
                    'reviews': [],
                    'portfolio_cases': [],
                    'seo_blocks': [],
                    'children': [],
                    'city_data': True,
                }
            )
            scores.append(score)
        if not scores:
            return 0
        return int(sum(scores) / len(scores))
    seo_score.short_description = 'SEO'


    def indexed_pages(self, obj):
        return ServicePage.objects.filter(city=obj, is_published=True, no_index=False).count()
    indexed_pages.short_description = 'Index'

    # =====================================================
    # NOINDEX
    # =====================================================

    def noindex_pages(self, obj):
        return ServicePage.objects.filter(city=obj, is_published=True, no_index=True).count()
    noindex_pages.short_description = 'Noindex'

    # =====================================================
    # WEAK PAGES
    # =====================================================

    def weak_pages(self, obj):

        pages = ServicePage.objects.filter(city=obj, is_published=True)
        weak = 0
        for page in pages:
            score = calculate_page_score(
                page,
                {
                    'faqs': [],
                    'reviews': [],
                    'portfolio_cases': [],
                    'seo_blocks': [],
                    'children': [],
                    'city_data': True,
                }
            )

            if score < 40:
                weak += 1
        return weak
    
    weak_pages.short_description = 'Weak'


    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        is_new = obj.pk is None

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if (
            is_new
            and form.cleaned_data.get(
                'copy_structure'
            )
        ):

            source_city = City.objects.filter(
                is_main=True,
                is_active=True
            ).first()

            if (
                source_city
                and source_city.id != obj.id
            ):

                copy_city_structure(
                    source_city=source_city,
                    target_city=obj
                )


    def get_fieldsets(self, request, obj=None):

        fieldsets = [
            (
                "Основное",
                {
                    "fields": (
                        "name",
                        "slug",
                        "name_where",
                        "name_oblast",
                        "name_oblast_where",
                        "is_active",
                        "is_rented",
                    )
                },
            ),
        ]

        if obj is None:
            fieldsets.append(
                (
                    "Копирование",
                    {
                        "fields": (
                            "copy_structure",
                        )
                    },
                )
            )

        fieldsets.extend([
            (
                "Контакты",
                {
                    "fields": (
                        "phone",
                        "address",
                        "price_text",
                        "telegram_chat_id",
                    )
                },
            ),
            (
                "SEO главной страницы города",
                {
                    "fields": (
                        "h1_title",
                        "seo_title",
                        "seo_description",
                        "seo_keywords",
                    )
                },
            ),
            (
                "Аренда",
                {
                    "fields": (
                        "rent_price",
                        "rented_until",
                    )
                },
            ),
        ])

        return fieldsets











