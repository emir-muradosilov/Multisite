from pages.models import SEOBlock



def copy_seo_blocks(
    source_city,
    target_city,
    page_map,
    replacer,
):
    """
    Копирование SEOBlock.

    Переносит:

    SEOBlock
        |
        ├── cities
        |
        └── services


    Восстанавливает ManyToMany связи
    на новые страницы.
    """


    for block in SEOBlock.objects.filter(
        cities=source_city
    ).distinct():


        new_block = SEOBlock.objects.create(
            title=replacer.replace(
                block.title
            ),

            block_type=block.block_type,

            content=replacer.replace(
                block.content
            ),

            is_active=block.is_active,

            sort_order=block.sort_order,
        )


        # город

        new_block.cities.add(
            target_city
        )


        # услуги

        old_services = block.services.all()


        for old_service in old_services:


            new_service = page_map.get(
                old_service.id
            )


            if new_service:

                new_block.services.add(
                    new_service
                )


    return True