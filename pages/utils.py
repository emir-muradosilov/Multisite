from django.urls import path

from .views import (
    home,
    service_page,
    faq_page,
    portfolio_case_page,
    district_service_page,
)

from .router import (
    resolve_one_level,
    resolve_two_levels,
)

urlpatterns = [

    # HOME
    path(
        "",
        home,
        name="home",
    ),

    # FAQ
    path(
        "faq/<slug:faq_slug>/",
        faq_page,
        name="faq_page",
    ),

    # Кейсы
    path(
        "<slug:city_slug>/cases/<slug:case_slug>/",
        portfolio_case_page,
        name="portfolio_case_page",
    ),

    # Районы
    path(
        "<slug:city_slug>/districts/<slug:district_slug>/<slug:service_slug>/",
        district_service_page,
        name="district_service_page",
    ),

    # Подстраницы города
    path(
        "<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/",
        service_page,
        name="service_subpage",
    ),

    # Страницы города
    path(
        "<slug:city_slug>/<slug:service_slug>/",
        service_page,
        name="service_page",
    ),

    # Москва:
    # /almaznoe-burenie/otverstiya/
    # Краснодар:
    # /krasnodar/almaznoe-burenie/
    path(
        "<slug:first>/<slug:second>/",
        resolve_two_levels,
        name="router_two_levels",
    ),

    # Москва:
    # /almaznoe-burenie/
    #
    # Города:
    # /krasnodar/
    path(
        "<slug:slug>/",
        resolve_one_level,
        name="router_one_level",
    ),
]