import re


class TextReplacer:
    """
    Замена текстов при создании нового города.

    Пример:

    Москва
    -> Краснодар

    Москве
    -> Краснодаре

    Московская область
    -> Краснодарский край


    Используется для:

    - title
    - h1
    - content
    - seo_title
    - seo_description
    - FAQ
    - CityData
    """


    def __init__(
        self,
        source_city,
        target_city,
    ):

        self.source_city = source_city
        self.target_city = target_city


        self.replacements = {

            # Москва
            source_city.name:
                target_city.name,


            # Москве
            source_city.name_where:
                target_city.name_where,


            # Московская область
            source_city.name_oblast:
                target_city.name_oblast,


            # Московской области
            source_city.name_oblast_where:
                target_city.name_oblast_where,
        }


    def replace(
        self,
        text,
    ):

        if not text:
            return text


        result = text


        # длинные фразы сначала
        # чтобы не было частичных замен

        replacements = sorted(
            self.replacements.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )


        for old, new in replacements:

            if not old:
                continue


            result = re.sub(
                re.escape(old),
                new,
                result,
                flags=re.IGNORECASE
            )


        return result