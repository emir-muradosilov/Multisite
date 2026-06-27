from django.urls import path
from .views import service_page, faq_page, home, portfolio_case_page, district_service_page, city_or_service


    
urlpatterns = [
    # HOME
    path('', home, name='home'),

    # Подуслуги Москвы
    path('<slug:service_slug>/<slug:page_slug>/', service_page, name='main_city_subservice'),

    # Москва
 #   path('<slug:service_slug>/', service_page, name='main_city_service'),
 #   path('<slug:service_slug>/<slug:page_slug>/', service_page, name='main_city_subservice'),



    path('<slug:city_slug>/faq/<slug:faq_slug>/', faq_page, name='faq_page'),
    path('<slug:city_slug>/cases/<slug:case_slug>/', portfolio_case_page, name='portfolio_case_page'),


    # Города
    path('<slug:city_slug>/<slug:service_slug>/', service_page, name='service_page'),
    path('<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/', service_page, name='service_subpage'),


    # Одноуровневые URL
    path('<slug:slug>/', city_or_service, name='city_or_service'),


    path('<slug:city_slug>/districts/<slug:district_slug>/<slug:service_slug>/',district_service_page, name='district_service_page'),
]


