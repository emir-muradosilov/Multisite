from django.urls import path
from .views import city_home

urlpatterns = [
    path('<slug:city_slug>/', city_home, name='city_home'),
]