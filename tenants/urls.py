from django.urls import path
from .views import tenant_dashboard, TenantLoginView, tenant_leads, tenant_settings, update_lead_status
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('dashboard/', tenant_dashboard, name='tenant_dashboard'),
    path('dashboard/leads/', tenant_leads, name='tenant_leads'),
    path('dashboard/settings/', tenant_settings, name='tenant_settings'),

    path('login/', TenantLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/leads/<int:lead_id>/status/', update_lead_status, name='update_lead_status'),
    
]