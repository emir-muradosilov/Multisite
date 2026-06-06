def get_canonical_url(
    request,
    page,
    page_score=None,
    district_page=False,
):

    current_url = request.build_absolute_uri(
        request.path
    )

    # =====================================================
    # DISTRICT PAGES
    # =====================================================

    if district_page:

        # weak district page
        if page_score and page_score < 50:

            return request.build_absolute_uri(
                page.service_page.get_absolute_url()
            )

        return current_url

    # =====================================================
    # NORMAL PAGES
    # =====================================================

    return current_url