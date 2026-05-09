from django.shortcuts import render

# Create your views here.
def seo_context(request):
    return {
        "canonical_url": request.build_absolute_uri(request.path)
    }