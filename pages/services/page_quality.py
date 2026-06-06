def calculate_page_score(page, context):

    score = 0

    # =====================================================
    # CONTENT
    # =====================================================

    content = page.content or ''

    if len(content) > 1500:
        score += 20

    elif len(content) > 800:
        score += 10

    # =====================================================
    # FAQ
    # =====================================================

    faqs = context.get('faqs')

    if faqs:

        faq_count = len(faqs)

        if faq_count >= 5:
            score += 15

        elif faq_count >= 2:
            score += 8

    # =====================================================
    # REVIEWS
    # =====================================================

    reviews = context.get('reviews')

    if reviews:

        review_count = len(reviews)

        if review_count >= 5:
            score += 15

        elif review_count >= 2:
            score += 8

    # =====================================================
    # CASES
    # =====================================================

    portfolio_cases = context.get(
        'portfolio_cases'
    )

    if portfolio_cases:

        case_count = len(portfolio_cases)

        if case_count >= 3:
            score += 15

        elif case_count >= 1:
            score += 8

    # =====================================================
    # SEO BLOCKS
    # =====================================================

    seo_blocks = context.get('seo_blocks')

    if seo_blocks and seo_blocks.exists():
        score += 10

    # =====================================================
    # CHILDREN
    # =====================================================

    children = context.get('children')

    if children and children.exists():
        score += 10

    # =====================================================
    # GEO
    # =====================================================

    city_data = context.get('city_data')

    if city_data:
        score += 10

    # =====================================================
    # SCHEMA
    # =====================================================

    score += 10

    return score