from django.db import transaction

from .replacer import TextReplacer

from .service_pages import copy_service_pages
#from .faq import copy_faq
from .city_data import copy_city_data
from .seo_blocks import copy_seo_blocks
from .portfolio import copy_portfolio



class CityCopier:
    """
    Полный движок копирования города.

    Создает новый город
    на основе эталонного.

    Копирует:

    ✓ ServicePage
    ✓ FAQ
    ✓ CityData
    ✓ SEOBlock
    ✓ PortfolioCase

    Автоматически заменяет:

    Москва
    ->
    Новый город

    """



    def __init__(
        self,
        source_city,
        target_city,
    ):

        self.source_city = source_city

        self.target_city = target_city


        self.replacer = TextReplacer(
            source_city,
            target_city,
        )


        # карта:

        # старый ServicePage
        #
        # ->
        #
        # новый ServicePage

        self.page_map = {}



    @transaction.atomic
    def run(self):


        # 1.
        # Услуги

        self.page_map = copy_service_pages(
            source_city=self.source_city,
            target_city=self.target_city,
            replacer=self.replacer,
        )



        # 2.
        # FAQ

        # 3.
        # Данные города

        copy_city_data(
            source_city=self.source_city,
            target_city=self.target_city,
            replacer=self.replacer,
        )



        # 4.
        # SEO блоки

        copy_seo_blocks(
            source_city=self.source_city,
            target_city=self.target_city,
            replacer=self.replacer,
            page_map=self.page_map,
        )



        # 5.
        # Портфолио

        copy_portfolio(
            source_city=self.source_city,
            target_city=self.target_city,
            replacer=self.replacer,
            page_map=self.page_map,
        )


        return self.target_city