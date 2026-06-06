from django.http import HttpResponse


def robots_txt(request):
    sitemap_url = request.build_absolute_uri('/sitemap.xml')

    lines = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        f"Sitemap: {sitemap_url}"
#        "Sitemap: https://yourdomain.ru/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")