from django.http import HttpResponse


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Sitemap: https://yourdomain.ru/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")