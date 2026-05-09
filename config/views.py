from django.http import HttpResponse


def robots_txt(request):
    return HttpResponse(f"""
User-agent: *
Allow: /

Sitemap: {request.scheme}://{request.get_host()}/sitemap.xml
""", content_type="text/plain")