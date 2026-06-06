from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TenantProfile


@admin.register(TenantProfile)
class TenantProfileAdmin(admin.ModelAdmin):

    list_display = (
        'city',
        'company_name',
        'phone',
        'is_active',
    )

    search_fields = (
        'company_name',
        'phone',
        'city__name',
    )

    list_filter = (
        'is_active',
    )
