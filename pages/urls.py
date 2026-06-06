from django.urls import path
from .views import service_page, faq_page, home, portfolio_case_page, district_service_page

urlpatterns = [
    # HOME
    path('', home, name='home'),
    # FAQ
    path('<slug:city_slug>/faq/<slug:faq_slug>/', faq_page, name='faq_page'),
    # CASES
    path('<slug:city_slug>/cases/<slug:case_slug>/', portfolio_case_page, name='portfolio_case_page'),

    # DISTRICTS
    path(
    '<slug:city_slug>/districts/<slug:district_slug>/<slug:service_slug>/',
    district_service_page,
    name='district_service_page'
),

    # SERVICE SUBPAGE
    path('<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/', service_page, name='service_subpage'),
    # SERVICE PAGE
    path('<slug:city_slug>/<slug:service_slug>/', service_page, name='service_page'),



    path('<slug:city_slug>/<slug:service_slug>/', service_page),
    path('<slug:city_slug>/<slug:service_slug>/<slug:page_slug>/', service_page),

    path('<slug:city_slug>/faq/<slug:faq_slug>/', faq_page),


]


