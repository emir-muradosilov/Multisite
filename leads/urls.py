from django.urls import path
from .views import create_lead, success

urlpatterns = [
    path('<slug:city_slug>/lead/', create_lead, name='create_lead'),
    path('success/', success, name='success'),
]



