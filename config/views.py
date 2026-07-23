from django.http import HttpResponse


def robots_txt(request):

    lines = [
        "User-Agent: *",
        "Allow: /",
        f"Sitemap: https://{request.get_host()}/sitemap.xml"
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )
