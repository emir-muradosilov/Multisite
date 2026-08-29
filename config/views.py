from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from cities.models import City
from core.models import SiteSettings

import os
from django.conf import settings
from django.http import FileResponse, Http404



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

def favicon_view(request):
    settings = SiteSettings.objects.first()
    if settings and settings.favicon:
            return FileResponse(settings.favicon.open("rb"), content_type="image/x-icon",)
    return HttpResponse(status=404)