from pages.services.page_quality import (
    calculate_page_score
)


def get_indexing_data(
    request,
    page,
    context,
    district_page=False
):

    score = calculate_page_score(
        page,
        context
    )

    quality_level = 'low'

    # =====================================================
    # QUALITY LEVELS
    # =====================================================

    if score >= 80:

        quality_level = 'high'

    elif score >= 50:

        quality_level = 'medium'

    # =====================================================
    # INDEX RULES
    # =====================================================

    should_index = False

    if quality_level == 'high':
        should_index = True

    if quality_level == 'medium':
        should_index = True

    # =====================================================
    # DISTRICT PAGES
    # =====================================================

    if district_page:

        # слабые районные страницы
        # лучше canonical на parent

        if score < 70:
            should_index = False

    # =====================================================
    # CANONICAL
    # =====================================================

    canonical_url = request.build_absolute_uri(
        request.path
    )

    # слабая district page
    if district_page and score < 70:

        canonical_url = request.build_absolute_uri(
            page.get_absolute_url()
        )

    return {
        'score': score,
        'quality_level': quality_level,
        'should_index': should_index,
        'canonical_url': canonical_url,
    }