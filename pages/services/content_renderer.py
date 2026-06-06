from pages.services.spintax import (
    process_spintax
)


def render_seo_content(content, city, city_data=None):

    replacements = {
        '{city}': city.name,
    }

    if city_data:

        replacements.update({
            '{districts}': city_data.districts,
            '{industrial_zones}': city_data.industrial_zones,
            '{typical_concrete}': city_data.typical_concrete,
            '{typical_thickness}': city_data.typical_thickness,
            '{price_range}': city_data.price_range,

            '{metro}': city_data.metro,
            '{streets}': city_data.streets,
            '{business_centers}': city_data.business_centers,
            '{residential_complexes}': city_data.residential_complexes,
        })

    for key, value in replacements.items():

        content = content.replace(
            key,
            value or ''
        )

    content = process_spintax(content)

    return content