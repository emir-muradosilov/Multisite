from pages.models import CityData

from .clone import clone_model



def copy_city_data(
    source_city,
    target_city,
    replacer,
):
    """
    Копирование SEO данных города.

    CityData:

    industrial_zones
    districts
    competitors
    portfolio
    streets
    business_centers
    residential_complexes
    и т.д.
    """



    try:

        source_data = CityData.objects.get(
            city=source_city
        )


    except CityData.DoesNotExist:

        return None



    new_data = clone_model(
        source_data,
        replacer=replacer,
        city=target_city,
    )


    return new_data