from django.urls import path
from .views import service_page, faq_page

urlpatterns = [
    path('<slug:city_slug>/faq/<slug:faq_slug>/', faq_page, name='faq_page'),
    path('<slug:city_slug>/<slug:service_slug>/', service_page),
    path('<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/', service_page),

    path('<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/', service_page, name='service_subpage'),

    path('<slug:city_slug>/<slug:service_slug>/', service_page, name='service_page'),


    path('<slug:city_slug>/faq/<slug:faq_slug>/', faq_page),
]


