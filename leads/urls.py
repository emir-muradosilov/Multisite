from django.urls import path
from .views import create_lead, success

urlpatterns = [
    path('<slug:city_slug>/lead/', create_lead, name='lead_page'),
    path('lead/create/', create_lead, name='lead_ajax'),
    path('success/', success, name='success'),
]



