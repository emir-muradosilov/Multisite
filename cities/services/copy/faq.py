from pages.models import FAQ


from .clone import clone_model



def copy_faq(
    source_city,
    target_city,
    replacer,
    page_map,
):
    """
    Копирование FAQ.

    Копирует:

    FAQ

    И восстанавливает:

    FAQ.related_services
        ->
    новые ServicePage
    """



    for faq in FAQ.objects.filter(
        city=source_city
    ):


        old_services = list(
            faq.related_services.all()
        )


        new_faq = clone_model(
            faq,
            replacer=replacer,
            city=target_city,
        )



        # -------------------------------------
        # ManyToMany related_services
        # -------------------------------------


        for old_service in old_services:


            new_service = page_map.get(
                old_service.id
            )


            if new_service:

                new_faq.related_services.add(
                    new_service
                )


    return True