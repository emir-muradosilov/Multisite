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
    resolve_three_levels,
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
    # Универсальный роутер (2 уровня)
    # Москва:
    # /almaznoe-burenie/podusluga/
    #
    # Город:
    # /krasnodar/
    # =====================================================

    path(
    "<slug:first>/<slug:second>/<slug:third>/",
    resolve_three_levels,
    name="router_three_levels",
),

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