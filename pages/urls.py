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

    # =====================================================
    # HOME
    # =====================================================

    path(
        "",
        home,
        name="home",
    ),

    # =====================================================
    # FAQ Москвы
    # /faq/mozhno-li-burit/
    # =====================================================

    path(
        "faq/<slug:faq_slug>/",
        faq_page,
        name="faq_page",
    ),

    # =====================================================
    # FAQ города
    # /krasnodar/faq/...
    # =====================================================

    path(
        "<slug:city_slug>/faq/<slug:faq_slug>/",
        faq_page,
        name="city_faq_page",
    ),

    # =====================================================
    # Кейсы
    # =====================================================

    path(
        "<slug:city_slug>/cases/<slug:case_slug>/",
        portfolio_case_page,
        name="portfolio_case_page",
    ),

    # =====================================================
    # Районы
    # =====================================================

    path(
        "<slug:city_slug>/districts/<slug:district_slug>/<slug:service_slug>/",
        district_service_page,
        name="district_service_page",
    ),

    # =====================================================
    # Подстраницы услуги города
    # /krasnodar/burenie/podusluga/
    # =====================================================

    path(
        "<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/",
        service_page,
        name="service_subpage",
    ),

    # =====================================================
    # Услуга города
    # /krasnodar/burenie/
    # =====================================================

    path(
        "<slug:city_slug>/<slug:service_slug>/",
        service_page,
        name="service_page",
    ),

    # =====================================================
    # Универсальный роутер (2 уровня)
    # Москва:
    # /almaznoe-burenie/podusluga/
    #
    # Город:
    # /krasnodar/
    # =====================================================

    path(
        "<slug:first>/<slug:second>/",
        resolve_two_levels,
        name="router_two_levels",
    ),

    # =====================================================
    # Универсальный роутер (1 уровень)
    # /krasnodar/
    # /almaznoe-burenie/
    # =====================================================

    path(
        "<slug:slug>/",
        resolve_one_level,
        name="router_one_level",
    ),
]