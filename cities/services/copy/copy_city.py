from .copier import CityCopier



def copy_city(
    source_city,
    target_city,
):
    """
    Главная функция клонирования города.

    Используется из admin.


    Пример:

    copy_city(
        source_city=Москва,
        target_city=Краснодар
    )

    """


    copier = CityCopier(
        source_city=source_city,
        target_city=target_city,
    )


    return copier.run()