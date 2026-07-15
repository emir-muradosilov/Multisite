from django.forms.models import model_to_dict

from pages.models import (
    ServicePage,
    FAQ,
    CityData,
)


# =====================================================
# TEXT REPLACER
# =====================================================

def replace_text(text, replacements):

    if not text:
        return text

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


# =====================================================
# SERVICE PAGES
# =====================================================

def copy_service_pages(
    source_city,
    target_city,
    replacements,
):

    page_map = {}

    # -------------------------
    # Родительские
    # -------------------------

    parents = ServicePage.objects.filter(
        city=source_city,
        parent__isnull=True,
    )

    for page in parents:

        new_page = ServicePage.objects.create(

            city=target_city,

            parent=None,

            title=replace_text(
                page.title,
                replacements,
            ),

            slug=page.slug,

            h1_title=replace_text(
                page.h1_title,
                replacements,
            ),

            content=replace_text(
                page.content,
                replacements,
            ),

            seo_title=replace_text(
                page.seo_title,
                replacements,
            ),

            seo_description=replace_text(
                page.seo_description,
                replacements,
            ),

            seo_keywords=replace_text(
                page.seo_keywords,
                replacements,
            ),

            template=page.template,

            sort_order=page.sort_order,

            is_published=page.is_published,

            show_in_menu=page.show_in_menu,

            no_index=page.no_index,

        )

        page_map[page.id] = new_page

    # -------------------------
    # Подстраницы
    # -------------------------

    children = ServicePage.objects.filter(
        city=source_city,
        parent__isnull=False,
    )

    for page in children:

        new_page = ServicePage.objects.create(

            city=target_city,

            parent=page_map[
                page.parent_id
            ],

            title=replace_text(
                page.title,
                replacements,
            ),

            slug=page.slug,

            h1_title=replace_text(
                page.h1_title,
                replacements,
            ),

            content=replace_text(
                page.content,
                replacements,
            ),

            seo_title=replace_text(
                page.seo_title,
                replacements,
            ),

            seo_description=replace_text(
                page.seo_description,
                replacements,
            ),

            seo_keywords=replace_text(
                page.seo_keywords,
                replacements,
            ),

            template=page.template,

            sort_order=page.sort_order,

            is_published=page.is_published,

            show_in_menu=page.show_in_menu,

            no_index=page.no_index,

        )

        page_map[page.id] = new_page

    return page_map


# =====================================================
# FAQ
# =====================================================
'''
def copy_faq(
    source_city,
    target_city,
    page_map,
    replacements,
):

    faqs = FAQ.objects.filter(
        city=source_city
    )

    for faq in faqs:

        new_faq = FAQ.objects.create(

            city=target_city,

            question=replace_text(
                faq.question,
                replacements,
            ),

            answer=replace_text(
                faq.answer,
                replacements,
            ),

            slug=faq.slug,

            seo_title=replace_text(
                faq.seo_title,
                replacements,
            ),

            seo_description=replace_text(
                faq.seo_description,
                replacements,
            ),

            is_published=faq.is_published,

        )

        related = []

        for page in faq.related_services.all():

            if page.id in page_map:
                related.append(
                    page_map[page.id]
                )

        new_faq.related_services.set(
            related
        )
'''

# =====================================================
# CITY DATA
# =====================================================

def copy_city_data(
    source_city,
    target_city,
    replacements,
):

    data = CityData.objects.filter(
        city=source_city
    ).first()

    if not data:
        return

    values = model_to_dict(
        data
    )

    values.pop("id", None)
    values.pop("city", None)

    for field, value in values.items():

        if isinstance(value, str):

            values[field] = replace_text(
                value,
                replacements,
            )

    CityData.objects.create(
        city=target_city,
        **values,
    )


# =====================================================
# MAIN
# =====================================================

def copy_city(
    source_city,
    target_city,
):

    replacements = {

        source_city.name:
            target_city.name,

        source_city.name_where:
            target_city.name_where,

        source_city.name_oblast:
            target_city.name_oblast,

        source_city.name_oblast_where:
            target_city.name_oblast_where,

    }

    page_map = copy_service_pages(
        source_city,
        target_city,
        replacements,
    )

    copy_faq(
        source_city,
        target_city,
        page_map,
        replacements,
    )

    copy_city_data(
        source_city,
        target_city,
        replacements,
    )



