from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /success/",
        "",
        "Sitemap: http://127.0.0.1:8000/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")