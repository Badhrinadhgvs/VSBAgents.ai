from url_geapp.models import DynamicPage
from django.shortcuts import render, get_object_or_404


def dynamic_page(request, slug):
    page = get_object_or_404(DynamicPage, slug=slug)
    return render(request, 'dynamic_page.html', {'page': page})