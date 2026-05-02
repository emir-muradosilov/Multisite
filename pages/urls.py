from django.urls import path
from .views import service_page, faq_page, city_home

urlpatterns = [
    path('<slug:city_slug>/<slug:page_slug>/', service_page, name='service_page'),
    path('<slug:city_slug>/faq/<slug:faq_slug>/', faq_page, name='faq_page'),
    path('<slug:city_slug>/', city_home, name='city_home')
]