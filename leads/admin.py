from django.contrib import admin
from leads.models import Lead

# Register your models here.
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):

    list_display = (
        'created_at',
        'city',
        'name',
        'phone',
        'service',
        'status',
        'utm_source',
    )

    list_filter = (
        'status',
        'city',
        'utm_source',
    )

    search_fields = (
        'name',
        'phone',
    )

    ordering = (
        '-created_at',
    )