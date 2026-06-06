from pages.models import ServicePage


def get_related_pages(page, city):

    # CHILD PAGE
    if page.parent:

        siblings = ServicePage.objects.filter(
            parent=page.parent,
            is_published=True
        ).exclude(
            id=page.id
        )[:6]

        return siblings

    # PARENT PAGE
    related = ServicePage.objects.filter(
        city=city,
        parent__isnull=True,
        is_published=True
    ).exclude(
        id=page.id
    )[:6]

    return related