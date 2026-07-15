from pages.models import PortfolioCase

from .clone import clone_model



def copy_portfolio(
    source_city,
    target_city,
    page_map,
    replacer,
):
    """
    Копирование портфолио.

    Переносит:

    PortfolioCase

    Восстанавливает:

    service_page
    """


    for case in PortfolioCase.objects.filter(
        city=source_city
    ):


        new_service = None


        if case.service_page:

            new_service = page_map.get(
                case.service_page.id
            )



        new_case = clone_model(
            case,
            replacer=replacer,

            city=target_city,

            service_page=new_service,

            # районы специально не переносим
            district=None,
        )


        return_case = new_case


    return True